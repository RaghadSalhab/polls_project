from polls.repositories.choice_repository import ChoiceRepository
from polls.repositories.question_repository import QuestionRepository
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from polls.schemas.choice import ChoiceSchema
from polls.cache_decorator import cache_response
from polls.cache import get_cache, set_cache, r  
class ChoiceService:

    @staticmethod
    @cache_response(lambda choice_id: f"choice:{choice_id}", expire=300)
    def get_choice(choice_id: int):
        choice = ChoiceRepository.get_choice(choice_id)
        if not choice:
            raise ObjectDoesNotExist("Choice not found")
        return ChoiceSchema().dump(choice)

    @staticmethod
    @cache_response(lambda question_id: f"choices:list:{question_id}", expire=120)
    def list_choices_for_question(question_id: int):
        question = QuestionRepository.get_question(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        
        choices = ChoiceRepository.list_choices_for_question(question_id)
        return ChoiceSchema(many=True).dump(choices)

    @staticmethod
    def create_choice(user, question_id: int, choice_text: str):
        question = QuestionRepository.get_question(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        if question.created_by_id != user.id:
            raise PermissionDenied("You cannot add choice to this question")

        choice = ChoiceRepository.create_choice(question_id, choice_text)

        r.delete(f"choices:list:{question_id}")
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

        r.delete(f"choice:{choice_id}")
        r.delete(f"choices:list:{choice.question.id}")
        return ChoiceSchema().dump(updated_choice)

    @staticmethod
    def delete_choice(user, choice_id: int):
        choice = ChoiceRepository.get_choice(choice_id)
        if not choice:
            raise ObjectDoesNotExist("Choice not found")
        if choice.question.created_by_id != user.id:
            raise PermissionDenied("You cannot delete this choice")

        ChoiceRepository.delete_choice(choice_id)

        r.delete(f"choice:{choice_id}")
        r.delete(f"choices:list:{choice.question.id}")

    @staticmethod
    def vote(choice_id: int):
        choice = ChoiceRepository.get_choice(choice_id)
        if not choice:
            raise ObjectDoesNotExist("Choice not found")

        choice.votes += 1
        from polls.models.database import Session
        Session.flush()
        Session.refresh(choice)
        
        r.delete(f"choice:{choice_id}")
        r.delete(f"choices:list:{choice.question.id}")
        return ChoiceSchema().dump(choice)
