# services/question_service.py
from polls.repositories.choice_repository import ChoiceRepository
from polls.repositories.question_repository import QuestionRepository
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

class QuestionService:

    @staticmethod
    def list_questions(session, search: str = None):
        return QuestionRepository.list_questions(session, search=search)

    @staticmethod
    def list_questions_for_user(session, user_id):
        user_id = int(user_id)
        return QuestionRepository.list_questions_for_user(session, user_id)

    @staticmethod
    def get_question(session, question_id: int):
        question = QuestionRepository.get_question(session, question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        return question

    @staticmethod
    def create_question(session, user, question_text: str, choices: list[str] = None):
        return QuestionRepository.create_question(session, user.id, question_text, choices)
    
    @staticmethod
    def update_question(session, user, question_id: int, question_text: str, choices: list[dict] = None):
        question = QuestionRepository.get_question(session, question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        if question.created_by_id != user.id:
            raise PermissionDenied("You cannot edit this question")
        return QuestionRepository.update_question(session, question_id, question_text, choices)

    @staticmethod
    def delete_question(session, user, question_id: int):
        question = QuestionRepository.get_question(session, question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        if question.created_by_id != user.id:
            raise PermissionDenied("You cannot delete this question")
        QuestionRepository.delete_question(session, question_id)
