# repositories/question_repository.py
from sqlalchemy.orm import Session, joinedload
from polls.models.question import Question
from polls.models.choice import Choice
from polls.models.database import SessionLocal
from polls.models.database import Base, engine

class QuestionRepository:

    @staticmethod
    def list_questions(search: str = None):
        with SessionLocal() as session:
            query = session.query(Question).options(joinedload(Question.choices))
            if search:
                query = query.filter(Question.question_text.ilike(f"%{search}%"))
            return query.all()

    def list_questions_for_user(user_id: int):
        with SessionLocal() as session:
            questions = session.query(Question)\
                            .filter(Question.created_by_id == user_id)\
                            .all()
            print(f"Found {len(questions)} questions for user {user_id}")
            return questions

    @staticmethod
    def get_question(question_id: int):
        with SessionLocal() as session:
            return session.query(Question)\
                        .options(joinedload(Question.created_by), joinedload(Question.choices))\
                        .filter(Question.id == question_id)\
                        .first()


    @staticmethod
    def create_question(user_id: int, question_text: str, choices: list[str] = None):
        with SessionLocal() as session:

            question = Question(created_by_id=user_id, question_text=question_text)
            session.add(question)
            session.flush()  

            if choices:
                for choice_text in choices:
                    choice = Choice(question_id=question.id, choice_text=choice_text, votes=0)
                    session.add(choice)

            session.commit()

            question = session.query(Question)\
                              .options(joinedload(Question.choices))\
                              .filter(Question.id == question.id)\
                              .first()
            return question

    @staticmethod
    def update_question(question_id: int, question_text: str, choices: list[dict] = None):
        with SessionLocal() as session:
            question = session.query(Question)\
                              .options(joinedload(Question.choices))\
                              .filter(Question.id == question_id)\
                              .first()
            if not question:
                return None

            question.question_text = question_text

            if choices is not None:
                for choice_data in choices:
                    choice_id = choice_data.get("id")
                    choice_text = choice_data.get("choice_text")

                    if choice_id:
                        choice = next((c for c in question.choices if c.id == choice_id), None)
                        if choice:
                            choice.choice_text = choice_text
                    else:
                        new_choice = Choice(question_id=question.id, choice_text=choice_text, votes=0)
                        session.add(new_choice)

            session.commit()

            question = session.query(Question)\
                              .options(joinedload(Question.choices))\
                              .filter(Question.id == question_id)\
                              .first()
            return question

    @staticmethod
    def delete_question(question_id: int):
        with SessionLocal() as session:
            question = session.query(Question).filter(Question.id == question_id).first()
            if question:
                session.delete(question)
                session.commit()