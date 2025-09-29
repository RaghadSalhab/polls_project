# services/stats_service.py
from polls.repositories.stats_repository import StatsRepository

class StatsService:

    @staticmethod
    def get_top_question(session):
        return StatsRepository.top_voted_question(session)

    @staticmethod
    def get_question_votes(session, question_id: int):
        return StatsRepository.question_votes(session, question_id)

    @staticmethod
    def get_top_choice(session):
        return StatsRepository.top_voted_choice(session)

    @staticmethod
    def list_questions_with_votes(session):
        return StatsRepository.all_questions_with_votes(session)
