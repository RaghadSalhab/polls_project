from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from polls.caches.choice_cache import ChoiceCache
from polls.repositories.choice_repository import ChoiceRepository
from polls.repositories.question_repository import QuestionRepository
from polls.schemas.choice import ChoiceSchema
from polls.models.database import Session

class ChoiceService:
    cache = ChoiceCache(client_name="choice_cache_client")

    @staticmethod
    def get_choice(choice_id: int):
        cached = ChoiceService.cache.get_by_id(choice_id)
        if cached:
            return cached

        choice = ChoiceRepository.get(choice_id)
        if not choice:
            raise ObjectDoesNotExist("Choice not found")

        data = ChoiceSchema().dump(choice)
        ChoiceService.cache.set_by_id(choice_id, data)
        return data

    @staticmethod
    def list_choices_for_question(question_id: int):
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
    def create_choice(user, question_id: int, choice_text: str):
        question = QuestionRepository.get(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        if question.created_by_id != user.id:
            raise PermissionDenied("You cannot add choice to this question")

        choice = ChoiceRepository.add(ChoiceRepository.model(question_id=question_id, choice_text=choice_text))
        ChoiceService.cache.delete_list_for_question(question_id)
        return ChoiceSchema().dump(choice)

    @staticmethod
    def update_choice(user, choice_id: int, choice_text: str):
        choice = ChoiceRepository.get(choice_id)
        if not choice:
            raise ObjectDoesNotExist("Choice not found")
        if choice.question.created_by_id != user.id:
            raise PermissionDenied("You cannot edit this choice")
        if choice.votes > 0:
            raise PermissionDenied("Cannot edit a choice after votes")

        choice.choice_text = choice_text
        Session.flush()
        Session.refresh(choice)

        ChoiceService.cache.delete_by_id(choice_id)
        ChoiceService.cache.delete_list_for_question(choice.question.id)
        return ChoiceSchema().dump(choice)

    @staticmethod
    def delete_choice(user, choice_id: int):
        choice = ChoiceRepository.get(choice_id)
        if not choice:
            raise ObjectDoesNotExist("Choice not found")
        if choice.question.created_by_id != user.id:
            raise PermissionDenied("You cannot delete this choice")

        ChoiceRepository.delete(choice)
        ChoiceService.cache.delete_by_id(choice_id)
        ChoiceService.cache.delete_list_for_question(choice.question.id)

    @staticmethod
    def vote(choice_id: int):
        choice = ChoiceRepository.vote(choice_id)
        if not choice:
            raise ObjectDoesNotExist("Choice not found")

        ChoiceService.cache.delete_by_id(choice_id)
        ChoiceService.cache.delete_list_for_question(choice.question.id)
        return ChoiceSchema().dump(choice)