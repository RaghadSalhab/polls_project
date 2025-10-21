from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from polls.elasticsearch.question_elasticsearch import QuestionElasticsearch
from polls.repositories.question_repository import QuestionRepository
from polls.schemas.question import QuestionSchema
from polls.caches.question_cache import QuestionCache
from polls.elasticsearch.log_elasticsearch import LogElasticsearch
from ddtrace import tracer
from polls.messaging.core.clients import sns
import json
from polls.messaging.core.event_publisher import EventPublisher

class QuestionService:
    cache = QuestionCache()
    es = QuestionElasticsearch()
    log_es = LogElasticsearch() 
    SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:000000000000:question-topic"

    @staticmethod
    def search_questions(keyword: str):
        with tracer.trace("question_service.search_questions"):
            cached = QuestionService.cache.get_list(f"search:{keyword}")
            if cached:
                QuestionService.log_es.log_event(
                    level="INFO",
                    action="SEARCH_CACHE_HIT",
                    object_type="QUESTION",
                    message=f"Search cache hit for keyword: '{keyword}'"
                )
                return cached

            results = QuestionService.es.search_questions(keyword)
            QuestionService.cache.set_list(f"search:{keyword}", results, expire=60)
            QuestionService.log_es.log_event(
                level="INFO",
                action="SEARCH",
                object_type="QUESTION",
                message=f"Performed search for keyword: '{keyword}'",
                details={"results_count": len(results)}
            )
            return results

    @staticmethod
    def get_question(question_id: int):
        with tracer.trace("question_service.get_question"):
            # cached = QuestionService.cache.get_by_id(question_id)
            # if cached:
            #     QuestionService.log_es.log_event(
            #         level="INFO",
            #         action="GET_CACHE_HIT",
            #         object_type="QUESTION",
            #         object_id=question_id,
            #         message=f"Fetched question from cache"
            #     )
            #     return cached

            question = QuestionRepository.get(question_id)
            if not question:
                QuestionService.log_es.log_event(
                    level="WARNING",
                    action="GET_FAIL",
                    object_type="QUESTION",
                    object_id=question_id,
                    message="Question not found"
                )
                raise ObjectDoesNotExist("Question not found")

            data = QuestionSchema().dump(question)
            QuestionService.cache.set_by_id(question_id, data)
            QuestionService.log_es.log_event(
                level="INFO",
                action="GET",
                object_type="QUESTION",
                object_id=question_id,
                message="Fetched question from DB"
            )
            return data

    @staticmethod
    def list_questions(search: str = None):
        with tracer.trace("question_service.list_questions"):
            key = search or "all"
            cached = QuestionService.cache.get_list(key)
            if cached:
                QuestionService.log_es.log_event(
                    level="INFO",
                    action="LIST_CACHE_HIT",
                    object_type="QUESTION",
                    message=f"Fetched question list from cache: key={key}"
                )
                return cached

            questions = QuestionRepository.list_questions(search)
            data = QuestionSchema(many=True).dump(questions)
            QuestionService.cache.set_list(key, data, expire=120)
            QuestionService.log_es.log_event(
                level="INFO",
                action="LIST",
                object_type="QUESTION",
                message=f"Fetched question list from DB: key={key}",
                details={"results_count": len(data)}
            )
            return data
        
    @staticmethod
    def create_question(user, question_text: str, choices: list[str] = None):
        with tracer.trace("question_service.create_question"):
            question = QuestionRepository.create_question(user.id, question_text)
            QuestionService.cache.delete_list("all")
            QuestionService.es.index_question(question)
            QuestionService.log_es.log_event(
                level="INFO",
                action="CREATE",
                object_type="QUESTION",
                object_id=question.id,
                message=f"User {user.username} created question",
                details={"question_text": question_text}
            )
            EventPublisher.publish_question_event(
                "QUESTION_CREATED",
                {
                    "question_id": question.id,
                    "user_id": user.id,
                    "question_text": question_text,
                    "choices": choices or []
                }
            )

            print("📤 SNS message published successfully to:", QuestionService.SNS_TOPIC_ARN)

            return QuestionSchema().dump(question)
                
    @staticmethod
    def update_question(user, question_id: int, question_text: str, choices: list[dict] = None):
        with tracer.trace("question_service.update_question"):
            question = QuestionRepository.get(question_id)
            if not question:
                QuestionService.log_es.log_event(
                    level="WARNING",
                    action="UPDATE_FAIL",
                    object_type="QUESTION",
                    object_id=question_id,
                    message="Question not found"
                )
                raise ObjectDoesNotExist("Question not found")
            if question.created_by_id != user.id:
                QuestionService.log_es.log_event(
                    level="WARNING",
                    action="UPDATE_FORBIDDEN",
                    object_type="QUESTION",
                    object_id=question_id,
                    message=f"User {user.username} cannot edit this question"
                )
                raise PermissionDenied("You cannot edit this question")

            question = QuestionRepository.update_question(question_id, question_text)
            QuestionService.cache.delete_by_id(question_id)
            QuestionService.cache.delete_list("all")
            QuestionService.es.update_question(question_id, {"question_text": question_text})
            QuestionService.log_es.log_event(
                level="INFO",
                action="UPDATE",
                object_type="QUESTION",
                object_id=question_id,
                message=f"User {user.username} updated question",
                details={"question_text": question_text}
            )
            EventPublisher.publish_question_event(
                "QUESTION_UPDATED",
                {
                    "question_id": question.id,
                    "user_id": user.id,
                    "question_text": question_text,
                    "choices": choices or []
                }
            )

            return QuestionSchema().dump(question)

    @staticmethod
    def delete_question(user, question_id: int):
        with tracer.trace("question_service.delete_question"):
            question = QuestionRepository.get(question_id)
            if not question:
                QuestionService.log_es.log_event(
                    level="WARNING",
                    action="DELETE_FAIL",
                    object_type="QUESTION",
                    object_id=question_id,
                    message="Question not found"
                )
                raise ObjectDoesNotExist("Question not found")
            if question.created_by_id != user.id:
                QuestionService.log_es.log_event(
                    level="WARNING",
                    action="DELETE_FORBIDDEN",
                    object_type="QUESTION",
                    object_id=question_id,
                    message=f"User {user.username} cannot delete this question"
                )
                raise PermissionDenied("You cannot delete this question")

            QuestionRepository.delete_by_id(question_id)
            QuestionService.cache.delete_by_id(question_id)
            QuestionService.cache.delete_list("all")
            QuestionService.es.delete_question(question_id)
            QuestionService.log_es.log_event(
                level="INFO",
                action="DELETE",
                object_type="QUESTION",
                object_id=question_id,
                message=f"User {user.username} deleted question"
            )
            EventPublisher.publish_question_event(
                "QUESTION_DELETED",
                {
                    "question_id": question_id,
                    "user_id": user.id
                }
            )

    @staticmethod
    def list_questions_for_user(user_id: int):
        with tracer.trace("question_service.list_questions_for_user"):
            key = f"user:{user_id}"
            cached = QuestionService.cache.get_list(key)
            if cached:
                QuestionService.log_es.log_event(
                    level="INFO",
                    action="LIST_USER_CACHE_HIT",
                    object_type="QUESTION",
                    message=f"Fetched question list for user {user_id} from cache"
                )
                return cached

            questions = QuestionRepository.list_questions_for_user(user_id)
            data = QuestionSchema(many=True).dump(questions)
            QuestionService.cache.set_list(key, data)
            QuestionService.log_es.log_event(
                level="INFO",
                action="LIST_USER",
                object_type="QUESTION",
                message=f"Fetched question list for user {user_id}",
                details={"results_count": len(data)}
            )
            return data
