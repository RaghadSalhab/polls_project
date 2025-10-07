# polls/services/choice_service.py
from polls.repositories.choice_repository import ChoiceRepository
from polls.repositories.question_repository import QuestionRepository
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from polls.schemas.choice import ChoiceSchema
from polls.services.cache_manager import get_cache_manager
from polls.models.database import Session

class ChoiceService:
    cache = get_cache_manager()

    @staticmethod
    def get_choice(choice_id: int):
        cache_key = f"choice:{choice_id}"
        cached_data = ChoiceService.cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        choice = ChoiceRepository.get_choice(choice_id)
        if not choice:
            raise ObjectDoesNotExist("Choice not found")

        data = ChoiceSchema().dump(choice)
        ChoiceService.cache.set(cache_key, data)
        return data

    @staticmethod
    def list_choices_for_question(question_id: int):
        question = QuestionRepository.get_question(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")

        cache_key = f"choices:list:{question_id}"
        cached_data = ChoiceService.cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        choices = ChoiceRepository.list_choices_for_question(question_id)
        data = ChoiceSchema(many=True).dump(choices)
        ChoiceService.cache.set(cache_key, data, expire=120)
        return data

    @staticmethod
    def create_choice(user, question_id: int, choice_text: str):
        question = QuestionRepository.get_question(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        if question.created_by_id != user.id:
            raise PermissionDenied("You cannot add choice to this question")

        choice = ChoiceRepository.create_choice(question_id, choice_text)

        ChoiceService.cache.delete(f"choices:list:{question_id}")
        return ChoiceSchema().dump(choice)

    @staticmethod
    def update_choice(user, choice_id: int, choice_text: str):
        choice = ChoiceRepository.get_choice(choice_id)
        if not choice:
            raise ObjectDoesNotExist("Choice not found")
        if choice.question.created_by_id != user.id:
            raise PermissionDenied("You cannot edit this choice")
        if choice.votes > 0:
            raise PermissionDenied("Cannot edit a choice after votes")

        updated_choice = ChoiceRepository.update_choice(choice_id, choice_text)

        ChoiceService.cache.delete(f"choice:{choice_id}")
        ChoiceService.cache.delete(f"choices:list:{choice.question.id}")
        return ChoiceSchema().dump(updated_choice)

    @staticmethod
    def delete_choice(user, choice_id: int):
        choice = ChoiceRepository.get_choice(choice_id)
        if not choice:
            raise ObjectDoesNotExist("Choice not found")
        if choice.question.created_by_id != user.id:
            raise PermissionDenied("You cannot delete this choice")

        ChoiceRepository.delete_choice(choice_id)

        ChoiceService.cache.delete(f"choice:{choice_id}")
        ChoiceService.cache.delete(f"choices:list:{choice.question.id}")

    @staticmethod
    def vote(choice_id: int):
        choice = ChoiceRepository.get_choice(choice_id)
        if not choice:
            raise ObjectDoesNotExist("Choice not found")

        choice.votes += 1
        Session.flush()
        Session.refresh(choice)

        ChoiceService.cache.delete(f"choice:{choice_id}")
        ChoiceService.cache.delete(f"choices:list:{choice.question.id}")
        return ChoiceSchema().dump(choice)
