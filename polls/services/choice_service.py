from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from polls.caches.choice_cache import ChoiceCache
from polls.messaging.core.event_publisher import EventPublisher
from polls.repositories.choice_repository import ChoiceRepository
from polls.repositories.question_repository import QuestionRepository
from polls.schemas.choice import ChoiceSchema
from polls.models.database import Session
from polls.elasticsearch.choice_elasticsearch import ChoiceElasticsearch
from polls.elasticsearch.log_elasticsearch import LogElasticsearch
from polls.messaging.core.clients import sns
import json
from ddtrace import tracer 


class ChoiceService:
    cache = ChoiceCache()
    es = ChoiceElasticsearch()  
    log_es = LogElasticsearch()  

    #this is the SNS Topic ARN for choice events
    SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:000000000000:choice-topic"

    @staticmethod
    def get_choice(choice_id: int):
        with tracer.trace("choice_service.get_choice"):
            # cached = ChoiceService.cache.get_by_id(choice_id)
            # if cached:
            #     return cached

            choice = ChoiceRepository.get(choice_id)
            if not choice:
                ChoiceService.log_es.log_event(
                    level="WARNING",
                    action="GET_FAIL",
                    object_type="CHOICE",
                    object_id=choice_id,
                    message="Choice not found"
                )
                raise ObjectDoesNotExist("Choice not found")

            data = ChoiceSchema().dump(choice)
            ChoiceService.cache.set_by_id(choice_id, data)
            return data

    @staticmethod
    def list_choices_for_question(question_id: int):
        with tracer.trace("choice_service.list_choices_for_question"):
            cached = ChoiceService.cache.get_list_for_question(question_id)
            if cached:
                return cached

            question = QuestionRepository.get(question_id)
            if not question:
                raise ObjectDoesNotExist("Question not found")

            choices = ChoiceRepository.list_choices_for_question(question_id)
            data = ChoiceSchema(many=True).dump(choices)
            ChoiceService.cache.set_list_for_question(question_id, data, expire=120)
            return data

    @staticmethod
    def create_choice(user_id, question_id: int, choice_text: str, publish_event: bool = True):
        with tracer.trace("choice_service.create_choice"):
            question = QuestionRepository.get(question_id)
            if not question:
                raise ObjectDoesNotExist("Question not found")
            if question.created_by_id != user_id:
                raise PermissionDenied("You cannot add choice to this question")

            choice = ChoiceRepository.add(
                ChoiceRepository.model(question_id=question_id, choice_text=choice_text)
            )
            Session.commit()

            ChoiceService.cache.delete_list_for_question(question_id)
            
            try:
                ChoiceService.es.index_choice(choice)
            except Exception as e:
                print(f"⚠️ Elasticsearch indexing failed (will retry): {e}")
            
            # ChoiceService.log_es.log_event(
            #     level="INFO",
            #     action="CREATE",
            #     object_type="CHOICE",
            #     object_id=choice.id,
            #     message=f"Choice created by user {user_id}",
            #     details={"choice_text": choice_text, "question_id": question_id}
            # )
            
            if publish_event:
                EventPublisher.publish_choice_event(
                    "CHOICE_CREATED",
                    {
                        "choice_id": choice.id,
                        "question_id": question_id,
                        "user_id": user_id,
                        "choice_text": choice_text
                    }
                )
            
            return ChoiceSchema().dump(choice)

    @staticmethod
    def update_choice(user_id, choice_id: int, choice_text: str, publish_event: bool = True):
        with tracer.trace("choice_service.update_choice"):
            choice = ChoiceRepository.get(choice_id)
            if not choice:
                raise ObjectDoesNotExist("Choice not found")
            if choice.question.created_by_id != user_id:
                raise PermissionDenied("You cannot edit this choice")
            if choice.votes > 0:
                raise PermissionDenied("Cannot edit a choice after votes")

            choice.choice_text = choice_text
            Session.commit()

            ChoiceService.cache.delete_by_id(choice_id)
            ChoiceService.cache.delete_list_for_question(choice.question.id)
            
            try:
                ChoiceService.es.update_choice(choice_id, {"choice_text": choice_text})
            except Exception as e:
                print(f"⚠️ Elasticsearch update failed (will retry): {e}")
            
            ChoiceService.log_es.log_event(
                level="INFO",
                action="UPDATE",
                object_type="CHOICE", 
                object_id=choice_id,
                message=f"Choice updated by user {user_id}",
                details={"choice_text": choice_text}
            )
            
            # if publish_event:
            #     EventPublisher.publish_choice_event(
            #         "CHOICE_UPDATED",
            #         {
            #             "choice_id": choice_id,
            #             "question_id": choice.question.id,
            #             "user_id": user_id,
            #             "choice_text": choice_text
            #         }
            #     )

        return ChoiceSchema().dump(choice)
    @staticmethod
    def delete_choice(user, choice_id: int):
        with tracer.trace("choice_service.delete_choice"):
            choice = ChoiceRepository.get(choice_id)
            if not choice:
                raise ObjectDoesNotExist("Choice not found")
            if choice.question.created_by_id != user.id:
                raise PermissionDenied("You cannot delete this choice")

            ChoiceRepository.delete(choice)
            ChoiceService.cache.delete_by_id(choice_id)
            ChoiceService.cache.delete_list_for_question(choice.question.id)
            ChoiceService.es.delete_choice(choice_id)
            ChoiceService.log_es.log_event(
                level="INFO",
                action="DELETE",
                object_type="CHOICE",
                object_id=choice_id,
                message=f"Choice deleted by user {user.id}"
            )
                        # --- SNS Publish ---
            EventPublisher.publish_choice_event(
                "CHOICE_DELETED",
                {
                    "choice_id": choice_id,
                    "question_id": choice.question.id,
                    "user_id": user.id
                }
            )

    @staticmethod
    def delete_choice_by_id(choice_id: int):
        with tracer.trace("choice_service.delete_choice_by_id"):
            choice = ChoiceRepository.get(choice_id)
            if not choice:
                raise ObjectDoesNotExist("Choice not found")

            ChoiceRepository.delete(choice)
            ChoiceService.cache.delete_by_id(choice_id)
            # ChoiceService.cache.delete_list_for_question(choice.question.id)
            ChoiceService.es.delete_choice(choice_id)
            ChoiceService.log_es.log_event(
                level="INFO",
                action="DELETE",
                object_type="CHOICE",
                object_id=choice_id,
                message=f"Choice deleted"
            )


    @staticmethod
    def vote(choice_id: int):
        with tracer.trace("choice_service.vote"):
            choice = ChoiceRepository.vote(choice_id)
            if not choice:
                raise ObjectDoesNotExist("Choice not found")

            ChoiceService.cache.delete_by_id(choice_id)
            ChoiceService.cache.delete_list_for_question(choice.question.id)
                        # --- SNS Publish ---
            EventPublisher.publish_choice_event(
                "CHOICE_VOTED",
                {
                    "choice_id": choice_id,
                    "question_id": choice.question.id
                }
            )
            
            return ChoiceSchema().dump(choice)

    @staticmethod
    def search_choices(keyword: str, question_id: int = None, page: int = 1, size: int = 10, fuzzy: bool = True):
        """Search choices in Elasticsearch, optionally filter by question_id"""
        cache_key = f"search:{question_id}:{keyword}"
        cached = ChoiceService.cache.get_list_for_question(cache_key)
        if cached:
            return cached

        results = ChoiceService.es.search_choices(keyword, page=page, size=size, fuzzy=fuzzy)

        if question_id:
            results = [r for r in results if r.get("question_id") == question_id]

        ChoiceService.cache.set_list_for_question(cache_key, results, expire=60)
        return results
