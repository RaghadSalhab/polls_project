from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from polls.repositories.choice_repository import ChoiceRepository
from polls.repositories.question_repository import QuestionRepository
from polls.schemas.choice import ChoiceSchema
from polls.services.cache_manager import get_cache_manager
from polls.models.database import Session

class ChoiceService:
    cache = get_cache_manager()

    # ---------------- Cache helpers ----------------
    @staticmethod
    def _get_from_cache(cache_key, fetch_fn, expire=None):
        cached_data = ChoiceService.cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        data = fetch_fn()
        if data is not None:
            ChoiceService.cache.set(cache_key, data, expire=expire)
        return data

    @staticmethod
    def _invalidate_choice_cache(choice):
        ChoiceService.cache.delete(f"choice:{choice.id}")
        ChoiceService.cache.delete(f"choices:list:{choice.question.id}")

    # ---------------- Choice operations ----------------
    @staticmethod
    def get_choice(choice_id: int):
        return ChoiceService._get_from_cache(
            f"choice:{choice_id}",
            lambda: ChoiceSchema().dump(ChoiceRepository.get(choice_id))
        )

    @staticmethod
    def list_choices_for_question(question_id: int):
        question = QuestionRepository.get(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")

        return ChoiceService._get_from_cache(
            f"choices:list:{question_id}",
            lambda: ChoiceSchema(many=True).dump(
                ChoiceRepository.list_choices_for_question(question_id)
            ),
            expire=120
        )

    @staticmethod
    def create_choice(user, question_id: int, choice_text: str):
        question = QuestionRepository.get(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        if question.created_by_id != user.id:
            raise PermissionDenied("You cannot add choice to this question")

        choice = ChoiceRepository.add(ChoiceRepository.model(question_id=question_id, choice_text=choice_text))
        ChoiceService.cache.delete(f"choices:list:{question_id}")
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
        ChoiceService._invalidate_choice_cache(choice)
        return ChoiceSchema().dump(choice)

    @staticmethod
    def delete_choice(user, choice_id: int):
        choice = ChoiceRepository.get(choice_id)
        if not choice:
            raise ObjectDoesNotExist("Choice not found")
        if choice.question.created_by_id != user.id:
            raise PermissionDenied("You cannot delete this choice")

        ChoiceRepository.delete(choice)
        ChoiceService._invalidate_choice_cache(choice)

    @staticmethod
    def vote(choice_id: int):
        choice = ChoiceRepository.vote(choice_id)
        if not choice:
            raise ObjectDoesNotExist("Choice not found")

        ChoiceService._invalidate_choice_cache(choice)
        return ChoiceSchema().dump(choice)
