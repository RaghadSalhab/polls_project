from sqlalchemy.orm import joinedload
from polls.models.database import Session
from polls.models.question import Question
from polls.repositories.base_repository import BaseRepository


class QuestionRepository(BaseRepository):
    model = Question

    @classmethod
    def list_questions(cls, search: str = None):
        query = Session.query(cls.model).options(joinedload(cls.model.choices))
        if search:
            query = query.filter(cls.model.question_text.ilike(f"%{search}%"))
        return query.all()

    @classmethod
    def list_questions_for_user(cls, user_id: int):
        questions = Session.query(cls.model).filter(cls.model.created_by_id == user_id).all()
        print(f"Found {len(questions)} questions for user {user_id}")
        return questions

    @classmethod
    def create_question(cls, user_id: int, question_text: str):
        question = cls.model(created_by_id=user_id, question_text=question_text)
        cls.add(question, commit=False)
        cls.commit()
        Session.refresh(question)
        Session.commit()  
        return question

    @classmethod
    def update_question(cls, question_id: int, question_text: str):
        question = cls.get(question_id)
        if not question:
            return None
        question.question_text = question_text
        cls.commit()
        Session.refresh(question)
        return question

    @classmethod
    def delete_question(cls, question_id: int):
        return cls.delete_by_id(question_id, commit=True)
