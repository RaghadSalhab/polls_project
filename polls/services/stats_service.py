# polls/services/stats_service.py
from polls.repositories.stats_repository import StatsRepository

class StatsService:

    @staticmethod
    def get_top_question():
        """
        يرجع السؤال الأكثر تصويتًا
        """
        return StatsRepository.top_voted_question()

    @staticmethod
    def get_question_votes(question_id):
        """
        يرجع مجموع الأصوات لسؤال معين
        """
        return StatsRepository.question_votes(question_id)

    @staticmethod
    def get_top_choice():
        """
        يرجع الخيار الأكثر تصويتًا
        """
        return StatsRepository.top_voted_choice()

    @staticmethod
    def list_questions_with_votes():
        """
        قائمة بكل الأسئلة مع مجموع أصواتها
        """
        return StatsRepository.all_questions_with_votes()
