# polls/services/poll_service.py
from polls.repositories.choice_repository import ChoiceRepository
from polls.repositories.question_repository import QuestionRepository
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied


class QuestionService:

    # ----------- Questions -----------

    @staticmethod
    def list_questions(search=None):
        return QuestionRepository.list_questions(search=search)

    @staticmethod
    def list_questions_for_user(user_id):
        return QuestionRepository.list_questions_for_user(user_id)

    @staticmethod
    def get_question(question_id):
        question = QuestionRepository.get_question(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        return question

    @staticmethod
    def create_question(user, question_text, choices=None):
        question = QuestionRepository.create_question(user, question_text)
        if choices:
            for choice_text in choices:
                ChoiceRepository.create_choice(question.id, choice_text)
        return question

    @staticmethod
    def update_question(user, question_id, question_text, choices=None):
        question = QuestionRepository.get_question(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")

        if question.created_by != user:
            raise PermissionDenied("You cannot edit this question")

        QuestionRepository.update_question(question_id, question_text)

        if choices:
            for choice_data in choices:
                choice_id = choice_data.get("id")
                choice_text = choice_data.get("choice_text")
                print(str(choice_id)+"  and   textt "+ choice_text)

                if choice_id:
                    choice = ChoiceRepository.get_choice(choice_id)
                    if choice and int(choice.question.id) == int(question_id):
                        ChoiceRepository.update_choice(choice_id, choice_text)
                else:
                    ChoiceRepository.create_choice(question_id, choice_text)

        return QuestionRepository.get_question(question_id)

    @staticmethod
    def delete_question(user, question_id):
        question = QuestionRepository.get_question(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        if question.created_by != user:
            raise PermissionDenied("You cannot delete this question")
        QuestionRepository.delete_question(question_id)

