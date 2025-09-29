# repositories/choice_repository.py
from sqlalchemy.orm import Session
from polls.repositories.user_repository import UserRepository
from polls.models.choice import Choice
from polls.models.question import Question
from polls.models.database import SessionLocal
from sqlalchemy.orm import Session, joinedload

class ChoiceRepository:

    @staticmethod
    def list_choices_for_question(question_id: int):
        with SessionLocal() as session:
            return session.query(Choice).filter(Choice.question_id == question_id).all()

    # @staticmethod
    # def get_choice(choice_id: int):
    #     with SessionLocal() as session:
    #         return session.query(Choice).filter(Choice.id == choice_id).join(Choice.question).first()
    @staticmethod
    def get_choice(choice_id: int):
        with SessionLocal() as session:
            return session.query(Choice)\
                          .options(joinedload(Choice.question))\
                          .filter(Choice.id == choice_id)\
                          .first()

    @staticmethod
    def create_choice(question_id: int, choice_text: str):
        with SessionLocal() as session:
            question = session.query(Question).filter(Question.id == question_id).first()
            if not question:
                return None
            choice = Choice(question_id=question.id, choice_text=choice_text)
            session.add(choice)
            session.commit()
            session.refresh(choice)   
            return choice

    @staticmethod
    def update_choice(choice_id: int, choice_text: str):
        with SessionLocal() as session:
            choice = session.query(Choice).filter(Choice.id == choice_id).first()
            if not choice:
                return None
            choice.choice_text = choice_text
            session.commit()
            session.refresh(choice)
            return choice
        
    @staticmethod
    def delete_choice(choice_id: int):
        with SessionLocal() as session:
            choice = session.query(Choice).filter(Choice.id == choice_id).first()
            if choice:
                session.delete(choice)
                session.commit()

    @staticmethod
    def vote(choice_id: int):
        with SessionLocal() as session:
            choice = session.query(Choice).filter(Choice.id == choice_id).first()
            if not choice:
                return None
            choice.votes += 1
            session.commit()
            session.refresh(choice)
            return choice
