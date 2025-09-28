# polls/services/poll_service.py
from polls.repositories.question_repository import QuestionRepository
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied


class PollService:

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
                QuestionRepository.create_choice(question.id, choice_text)
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
                    choice = QuestionRepository.get_choice(choice_id)
                    if choice and int(choice.question.id) == int(question_id):
                        QuestionRepository.update_choice(choice_id, choice_text)
                else:
                    QuestionRepository.create_choice(question_id, choice_text)

        return QuestionRepository.get_question(question_id)

    @staticmethod
    def delete_question(user, question_id):
        question = QuestionRepository.get_question(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        if question.created_by != user:
            raise PermissionDenied("You cannot delete this question")
        QuestionRepository.delete_question(question_id)

    # ----------- Choices -----------

    @staticmethod
    def list_choices_for_question(question_id):
        question = QuestionRepository.get_question(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        return QuestionRepository.list_choices_for_question(question_id)

    @staticmethod
    def create_choice(user, question_id, choice_text):
        question = QuestionRepository.get_question(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        if question.created_by != user:
            raise PermissionDenied("You cannot add choice to this question")
        return QuestionRepository.create_choice(question_id, choice_text)

    @staticmethod
    def update_choice(user, choice_id, choice_text):
        choice = QuestionRepository.get_choice(choice_id)
        if not choice:
            raise ObjectDoesNotExist("Choice not found")
        if choice.question.created_by != user:
            raise PermissionDenied("You cannot edit this choice")
        if choice.votes > 0:
            raise PermissionDenied("Cannot edit a choice after votes")
        return QuestionRepository.update_choice(choice_id, choice_text)

    @staticmethod
    def get_choice(choice_id):
        choice = QuestionRepository.get_choice(choice_id)
        if not choice:
            raise ObjectDoesNotExist("Choice not found")
        return choice
    
    @staticmethod
    def delete_choice(user, choice_id):
        choice = QuestionRepository.get_choice(choice_id)
        if not choice:
            raise ObjectDoesNotExist("Choice not found")
        if choice.question.created_by != user:
            raise PermissionDenied("You cannot delete this choice")
        QuestionRepository.delete_choice(choice_id)

    # ----------- Voting -----------

    @staticmethod
    def vote(choice_id):
        choice = QuestionRepository.get_choice(choice_id)
        if not choice:
            raise ObjectDoesNotExist("Choice not found")
        return QuestionRepository.vote(choice_id)
