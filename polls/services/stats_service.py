from decimal import Decimal
from polls.repositories.stats_repository import StatsRepository
from polls.schemas.question import QuestionSchema
from polls.schemas.choice import ChoiceSchema
from polls.caches.stats_cache import StatsCache

class StatsService:
    cache = StatsCache()

    @staticmethod
    def get_top_question():
        cached_data = StatsService.cache.get_top_question()
        if cached_data is not None:
            return cached_data

        question = StatsRepository.top_voted_question()
        if not question:
            return None

        data = QuestionSchema().dump(question)
        StatsService.cache.set_top_question(data, expire=300) 
        return data

    @staticmethod
    def get_question_votes(question_id: int):
        cached_data = StatsService.cache.get_question_votes(question_id)
        if cached_data is not None:
            return cached_data

        votes = StatsRepository.question_votes(question_id)
        votes_int = int(votes) if isinstance(votes, Decimal) else votes
        StatsService.cache.set_question_votes(question_id, votes_int, expire=300)
        return votes_int

    @staticmethod
    def get_top_choice():
        cached_data = StatsService.cache.get_top_choice()
        if cached_data is not None:
            return cached_data

        choice = StatsRepository.top_voted_choice()
        if not choice:
            return None

        data = ChoiceSchema().dump(choice)
        StatsService.cache.set_top_choice(data, expire=300)
        return data

    @staticmethod
    def list_questions_with_votes():
        cached_data = StatsService.cache.get_questions_with_votes()
        if cached_data is not None:
            return cached_data

        results = StatsRepository.all_questions_with_votes()
        data = [
            {"question": QuestionSchema().dump(q), "total_votes": total_votes}
            for q, total_votes in results
        ]
        StatsService.cache.set_questions_with_votes(data, expire=300)
        return data
