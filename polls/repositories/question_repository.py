from sqlalchemy.orm import joinedload
from polls.models.choice import Choice
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
    def create_question(cls, user_id: int, question_text: str, choices: list[str] = None):
        question = cls.model(created_by_id=user_id, question_text=question_text)
        cls.add(question, commit=False)

        if choices:
            for choice_text in choices:
                choice = Choice(question_id=question.id, choice_text=choice_text, votes=0)
                Session.add(choice)

        cls.commit()
        Session.refresh(question)
        return question

    @classmethod
    def update_question(cls, question_id: int, question_text: str, choices: list[dict] = None):
        question = cls.get(question_id)
        if not question:
            return None

        question.question_text = question_text
        if choices:
            for choice_data in choices:
                choice_id = choice_data.get("id")
                choice_text = choice_data.get("choice_text")
                if choice_id:
                    choice = next((c for c in question.choices if c.id == choice_id), None)
                    if choice:
                        choice.choice_text = choice_text
                else:
                    new_choice = Choice(question_id=question.id, choice_text=choice_text, votes=0)
                    Session.add(new_choice)

        cls.commit()
        Session.refresh(question)
        return question

    @classmethod
    def delete_question(cls, question_id: int):
        return cls.delete_by_id(question_id, commit=True)
