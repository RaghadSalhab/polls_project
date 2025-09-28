# polls/repositories/stats_repository.py
from polls.models.question import Question
from polls.models.choice import Choice
from django.db.models import Sum

class StatsRepository:

    @staticmethod
    def top_voted_question():
        return Question.objects.annotate(total_votes=Sum('choices__votes')) \
                               .order_by('-total_votes') \
                               .first()

    @staticmethod
    def question_votes(question_id):
        return Choice.objects.filter(question_id=question_id).aggregate(total_votes=Sum('votes'))['total_votes'] or 0

    @staticmethod
    def top_voted_choice():
        return Choice.objects.order_by('-votes').first()

    @staticmethod
    def all_questions_with_votes():
        return Question.objects.annotate(total_votes=Sum('choices__votes')).order_by('-total_votes')
