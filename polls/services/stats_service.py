from polls.repositories.stats_repository import StatsRepository

class StatsService:

    @staticmethod
    def get_top_question():
        return StatsRepository.top_voted_question()

    @staticmethod
    def get_question_votes( question_id: int):
        return StatsRepository.question_votes( question_id)

    @staticmethod
    def get_top_choice():
        return StatsRepository.top_voted_choice()

    @staticmethod
    def list_questions_with_votes():
        return StatsRepository.all_questions_with_votes()
