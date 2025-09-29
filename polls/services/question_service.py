# services/question_service.py
from polls.repositories.choice_repository import ChoiceRepository
from polls.repositories.question_repository import QuestionRepository
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

class QuestionService:

    # ----------- Questions -----------

    @staticmethod
    def list_questions(search: str = None):
        return QuestionRepository.list_questions(search=search)

 # services/question_service.py
    @staticmethod
    def list_questions_for_user(user_id):
        # حول أي شيء يوصلك لـ int
        user_id = int(user_id)
        return QuestionRepository.list_questions_for_user(user_id)


    @staticmethod
    def get_question(question_id: int):
        question = QuestionRepository.get_question(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        return question

    @staticmethod
    def create_question(user, question_text: str, choices: list[str] = None):
        question = QuestionRepository.create_question(user.id, question_text, choices)
        return question
    
    @staticmethod
    def update_question(user, question_id: int, question_text: str, choices: list[dict] = None):
        question = QuestionRepository.get_question(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")

        if question.created_by_id != user.id:
            raise PermissionDenied("You cannot edit this question")

        return QuestionRepository.update_question(question_id, question_text, choices)

    @staticmethod
    def delete_question(user, question_id: int):
        question = QuestionRepository.get_question(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        if question.created_by_id != user.id:
            raise PermissionDenied("You cannot delete this question")
        QuestionRepository.delete_question(question_id)
