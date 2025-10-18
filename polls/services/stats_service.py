from decimal import Decimal
from polls.repositories.stats_repository import StatsRepository
from polls.schemas.question import QuestionSchema
from polls.schemas.choice import ChoiceSchema
from polls.caches.stats_cache import StatsCache
from polls.messaging.clients import sns 
from ddtrace import tracer
import json
class StatsService:
    cache = StatsCache()
    SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:000000000000:StatsEvents"

    @staticmethod
    def get_top_question():
        with tracer.trace("stats_service.get_top_question"):
            question = StatsRepository.top_voted_question()
            if not question:
                return None

            data = QuestionSchema().dump(question)
            return data

    @staticmethod
    def get_question_votes(question_id: int):
        with tracer.trace("stats_service.get_question_votes"):

            votes = StatsRepository.question_votes(question_id)
            votes_int = int(votes) if isinstance(votes, Decimal) else votes
            return votes_int

    @staticmethod
    def get_top_choice():
        with tracer.trace("stats_service.get_top_choice"):

            choice = StatsRepository.top_voted_choice()
            if not choice:
                return None
            data = ChoiceSchema().dump(choice)
            return data

    @staticmethod
    def list_questions_with_votes():
        with tracer.trace("stats_service.list_questions_with_votes"):

            results = StatsRepository.all_questions_with_votes()
            data = [
                {"question": QuestionSchema().dump(q), "total_votes": total_votes}
                for q, total_votes in results
            ]
            return data
