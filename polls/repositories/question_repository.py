# polls/repositories/question_repository.py
from polls.models.choice import Choice
from django.core.exceptions import ObjectDoesNotExist
from polls.models.question import Question

class QuestionRepository:

    # ----------- Questions -----------

    @staticmethod
    def list_questions(search=None):
        qs = Question.objects.all().prefetch_related('choices')
        if search:
            qs = qs.filter(question_text__icontains=search)
        return qs

    @staticmethod
    def list_questions_for_user(user_id):
        return Question.objects.filter(created_by_id=user_id).prefetch_related('choices')

    @staticmethod
    def get_question(question_id):
        try:
            return Question.objects.prefetch_related('choices').get(id=question_id)
        except Question.DoesNotExist:
            return None

    @staticmethod
    def create_question(user, question_text):
        return Question.objects.create(created_by=user, question_text=question_text)

    @staticmethod
    def update_question(question_id, question_text):
        question = Question.objects.get(id=question_id)
        question.question_text = question_text
        question.save()
        return question

    @staticmethod
    def delete_question(question_id):
        Question.objects.filter(id=question_id).delete()
