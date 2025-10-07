# polls/services/question_service.py
import json
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from polls.repositories.question_repository import QuestionRepository
from polls.schemas.question import QuestionSchema
from polls.services.cache_manager import get_cache_manager

class QuestionService:
    cache = get_cache_manager()

    @staticmethod
    def get_question(question_id: int):
        cache_key = f"question:{question_id}"
        cached_data = QuestionService.cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        question = QuestionRepository.get_question(question_id)
        if not question:
            return None

        data = QuestionSchema().dump(question)
        QuestionService.cache.set(cache_key, data)
        return data

    @staticmethod
    def list_questions(search: str = None):
        cache_key = f"questions:list:{search or 'all'}"
        cached_data = QuestionService.cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        questions = QuestionRepository.list_questions(search)
        data = QuestionSchema(many=True).dump(questions)
        QuestionService.cache.set(cache_key, data, expire=120)
        return data

    @staticmethod
    def create_question(user, question_text: str, choices: list[str] = None):
        question = QuestionRepository.create_question(user.id, question_text, choices)

        QuestionService.cache.delete("questions:list:all")
        return QuestionSchema().dump(question)

    @staticmethod
    def update_question(user, question_id: int, question_text: str, choices: list[dict] = None):
        question = QuestionRepository.get_question(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        if question.created_by_id != user.id:
            raise PermissionDenied("You cannot edit this question")

        question = QuestionRepository.update_question(question_id, question_text, choices)

        QuestionService.cache.delete("questions:list:all")
        QuestionService.cache.delete(f"question:{question_id}")
        return QuestionSchema().dump(question)

    @staticmethod
    def delete_question(user, question_id: int):
        question = QuestionRepository.get_question(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        if question.created_by_id != user.id:
            raise PermissionDenied("You cannot delete this question")

        QuestionRepository.delete_question(question_id)
        QuestionService.cache.delete(f"question:{question_id}")
        QuestionService.cache.delete("questions:list:all")

    @staticmethod
    def list_questions_for_user(user_id: int):
        cache_key = f"user:{user_id}:questions"
        cached_data = QuestionService.cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        questions = QuestionRepository.list_questions_for_user(user_id)
        data = QuestionSchema(many=True).dump(questions)
        QuestionService.cache.set(cache_key, data)
        return data
