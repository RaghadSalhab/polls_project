from polls.repositories.choice_repository import ChoiceRepository
from polls.repositories.question_repository import QuestionRepository
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from polls.models.database import Session

class ChoiceService:

    @staticmethod
    def list_choices_for_question(question_id: int):
        question = QuestionRepository.get_question(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        return ChoiceRepository.list_choices_for_question(question_id)

    @staticmethod
    def create_choice(user, question_id: int, choice_text: str):
        question = QuestionRepository.get_question(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        if question.created_by_id != user.id:
            raise PermissionDenied("You cannot add choice to this question")
        return ChoiceRepository.create_choice(question_id, choice_text)

    @staticmethod
    def update_choice(user, choice_id: int, choice_text: str):
        choice = ChoiceRepository.get_choice(choice_id)
        if not choice:
            raise ObjectDoesNotExist("Choice not found")
        if choice.question.created_by_id != user.id:
            raise PermissionDenied("You cannot edit this choice")
        if choice.votes > 0:
            raise PermissionDenied("Cannot edit a choice after votes")
        return ChoiceRepository.update_choice(choice_id, choice_text)

    @staticmethod
    def get_choice(choice_id: int):
        choice = ChoiceRepository.get_choice(choice_id)
        if not choice:
            raise ObjectDoesNotExist("Choice not found")
        return choice

    @staticmethod
    def delete_choice(user, choice_id: int):
        choice = ChoiceRepository.get_choice(choice_id)
        if not choice:
            raise ObjectDoesNotExist("Choice not found")
        if choice.question.created_by_id != user.id:
            raise PermissionDenied("You cannot delete this choice")
        ChoiceRepository.delete_choice(choice_id)

    @staticmethod
    def vote(choice_id: int):
        choice = ChoiceRepository.get_choice(choice_id)
        if not choice:
            raise ObjectDoesNotExist("Choice not found")
        choice.votes += 1
        Session.flush()
        Session.refresh(choice)
        return choice
