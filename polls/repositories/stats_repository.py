# repositories/stats_repository.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from polls.models.question import Question
from polls.models.choice import Choice
from polls.models.database import SessionLocal
from sqlalchemy.orm import joinedload
from sqlalchemy import func
class StatsRepository:

    @staticmethod
    def top_voted_question(session):
        question = session.query(Question)\
            .options(joinedload(Question.choices))\
            .outerjoin(Question.choices)\
            .group_by(Question.id)\
            .order_by(func.coalesce(func.sum(Choice.votes), 0).desc())\
            .limit(1)\
            .first()
        return question

    @staticmethod
    def question_votes(session, question_id: int):
        total = session.query(func.coalesce(func.sum(Choice.votes), 0))\
                       .filter(Choice.question_id == question_id)\
                       .scalar()
        return total

    @staticmethod
    def top_voted_choice(session):
        return session.query(Choice).order_by(Choice.votes.desc()).first()

    @staticmethod
    def all_questions_with_votes(session):
        return session.query(
            Question,
            func.coalesce(func.sum(Choice.votes), 0).label('total_votes')
        )\
        .outerjoin(Choice, Choice.question_id == Question.id)\
        .group_by(Question.id)\
        .order_by(func.desc('total_votes'))\
        .all()
