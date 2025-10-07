from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from polls.repositories.question_repository import QuestionRepository
from polls.schemas.question import QuestionSchema
from polls.caches.question_cache import QuestionCache

class QuestionService:
    cache = QuestionCache(client_name="question_cache_client")

    @staticmethod
    def get_question(question_id: int):
        cached = QuestionService.cache.get_by_id(question_id)
        if cached:
            return cached

        question = QuestionRepository.get(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")

        data = QuestionSchema().dump(question)
        QuestionService.cache.set_by_id(question_id, data)
        return data

    @staticmethod
    def list_questions(search: str = None):
        key = search or "all"
        cached = QuestionService.cache.get_list(key)
        if cached:
            return cached

        questions = QuestionRepository.list_questions(search)
        data = QuestionSchema(many=True).dump(questions)
        QuestionService.cache.set_list(key, data, expire=120)
        return data

    @staticmethod
    def create_question(user, question_text: str, choices: list[str] = None):
        question = QuestionRepository.create_question(user.id, question_text, choices)
        QuestionService.cache.delete_list("all")
        return QuestionSchema().dump(question)

    @staticmethod
    def update_question(user, question_id: int, question_text: str, choices: list[dict] = None):
        question = QuestionRepository.get(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        if question.created_by_id != user.id:
            raise PermissionDenied("You cannot edit this question")

        question = QuestionRepository.update_question(question_id, question_text, choices)
        QuestionService.cache.delete_by_id(question_id)
        QuestionService.cache.delete_list("all")
        return QuestionSchema().dump(question)

    @staticmethod
    def delete_question(user, question_id: int):
        question = QuestionRepository.get(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        if question.created_by_id != user.id:
            raise PermissionDenied("You cannot delete this question")

        QuestionRepository.delete(question_id)
        QuestionService.cache.delete_by_id(question_id)
        QuestionService.cache.delete_list("all")

    @staticmethod
    def list_questions_for_user(user_id: int):
        key = f"user:{user_id}"
        cached = QuestionService.cache.get_list(key)
        if cached:
            return cached

        questions = QuestionRepository.list_questions_for_user(user_id)
        data = QuestionSchema(many=True).dump(questions)
        QuestionService.cache.set_list(key, data)
        return data
