from decimal import Decimal
from polls.repositories.stats_repository import StatsRepository
from polls.cache_decorator import cache_response
from polls.schemas.question import QuestionSchema
from polls.schemas.choice import ChoiceSchema

class StatsService:

    @staticmethod
    @cache_response(lambda: "stats:top_question", expire=300)
    def get_top_question():
        question = StatsRepository.top_voted_question()
        if not question:
            return None
        return QuestionSchema().dump(question)

    @staticmethod
    @cache_response(lambda question_id: f"stats:question_votes:{question_id}", expire=300)
    def get_question_votes(question_id: int):
        votes = StatsRepository.question_votes(question_id)
        return int(votes) if isinstance(votes, Decimal) else votes

    @staticmethod
    @cache_response(lambda: "stats:top_choice", expire=300)
    def get_top_choice():
        choice = StatsRepository.top_voted_choice()
        if not choice:
            return None
        return ChoiceSchema().dump(choice)

    @staticmethod
    @cache_response(lambda: "stats:questions_with_votes", expire=300)
    def list_questions_with_votes():
        results = StatsRepository.all_questions_with_votes()
        data = [
            {
                "question": QuestionSchema().dump(q),
                "total_votes": total_votes,
            }
            for q, total_votes in results
        ]
        return data
