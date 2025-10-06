import json
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from polls.repositories.question_repository import QuestionRepository
from polls.schemas.question import QuestionSchema
from polls.services.redis_client import r
from polls.cache_decorator import cache_response
class QuestionService:

    @staticmethod
    @cache_response(lambda question_id: f"question:{question_id}", expire=300)
    def get_question(question_id: int):
        question = QuestionRepository.get_question(question_id)
        if not question:
            return None
        return QuestionSchema().dump(question)

    @staticmethod
    def list_questions(search: str = None):
        cache_key = f"questions:list:{search or 'all'}"
        cached_data = r.get(cache_key)
        if cached_data:
            print(f"📦 Cache hit for {cache_key}")
            return json.loads(cached_data)

        print(f"📦 Cache miss for {cache_key}, fetching from DB...")
        questions = QuestionRepository.list_questions(search)
        data = QuestionSchema(many=True).dump(questions)
        r.set(cache_key, json.dumps(data, default=str), ex=120)
        return data

    @staticmethod
    def create_question(user, question_text: str, choices: list[str] = None):
        question = QuestionRepository.create_question(user.id, question_text, choices)
        r.delete("questions:list:all")
        return QuestionSchema().dump(question)

    @staticmethod
    def update_question(user, question_id: int, question_text: str, choices: list[dict] = None):
        question = QuestionRepository.get_question(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        if question.created_by_id != user.id:
            raise PermissionDenied("You cannot edit this question")

        question = QuestionRepository.update_question(question_id, question_text, choices)
        r.set(f"question:{question_id}", json.dumps(QuestionSchema().dump(question), default=str), ex=300)
        r.delete("questions:list:all")
        return QuestionSchema().dump(question)

    @staticmethod
    def delete_question(user, question_id: int):
        question = QuestionRepository.get_question(question_id)
        if not question:
            raise ObjectDoesNotExist("Question not found")
        if question.created_by_id != user.id:
            raise PermissionDenied("You cannot delete this question")

        QuestionRepository.delete_question(question_id)
        r.delete(f"question:{question_id}")
        r.delete("questions:list:all")

    @staticmethod
    @cache_response(lambda user_id: f"user:{user_id}:questions", expire=300)
    def list_questions_for_user(user_id: int):
        questions = QuestionRepository.list_questions_for_user(user_id)
        return QuestionSchema(many=True).dump(questions)