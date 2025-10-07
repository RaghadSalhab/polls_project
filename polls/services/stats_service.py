# polls/services/stats_service.py
from decimal import Decimal
from polls.repositories.stats_repository import StatsRepository
from polls.schemas.question import QuestionSchema
from polls.schemas.choice import ChoiceSchema
from polls.services.cache_manager import get_cache_manager

class StatsService:
    cache = get_cache_manager()

    @staticmethod
    def get_top_question():
        cache_key = "stats:top_question"
        cached_data = StatsService.cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        question = StatsRepository.top_voted_question()
        if not question:
            return None

        data = QuestionSchema().dump(question)
        StatsService.cache.set(cache_key, data)
        return data

    @staticmethod
    def get_question_votes(question_id: int):
        cache_key = f"stats:question_votes:{question_id}"
        cached_data = StatsService.cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        votes = StatsRepository.question_votes(question_id)
        votes_int = int(votes) if isinstance(votes, Decimal) else votes
        StatsService.cache.set(cache_key, votes_int)
        return votes_int

    @staticmethod
    def get_top_choice():
        cache_key = "stats:top_choice"
        cached_data = StatsService.cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        choice = StatsRepository.top_voted_choice()
        if not choice:
            return None

        data = ChoiceSchema().dump(choice)
        StatsService.cache.set(cache_key, data)
        return data

    @staticmethod
    def list_questions_with_votes():
        cache_key = "stats:questions_with_votes"
        cached_data = StatsService.cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        results = StatsRepository.all_questions_with_votes()
        data = [
            {
                "question": QuestionSchema().dump(q),
                "total_votes": total_votes,
            }
            for q, total_votes in results
        ]
        StatsService.cache.set(cache_key, data)
        return data
