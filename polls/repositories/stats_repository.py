from sqlalchemy.orm import joinedload
from sqlalchemy import func
from polls.models.question import Question
from polls.models.choice import Choice
from polls.models.database import Session

class StatsRepository:

    @staticmethod
    def top_voted_question():
        return (
            Session.query(Question)
            .options(joinedload(Question.choices))
            .outerjoin(Question.choices)
            .group_by(Question.id)
            .order_by(func.coalesce(func.sum(Choice.votes), 0).desc())
            .limit(1)
            .first()
        )

    @staticmethod
    def question_votes(question_id: int):
        return (
            Session.query(func.coalesce(func.sum(Choice.votes), 0))
            .filter(Choice.question_id == question_id)
            .scalar()
        )

    @staticmethod
    def top_voted_choice():
        return Session.query(Choice).order_by(Choice.votes.desc()).first()

    @staticmethod
    def all_questions_with_votes():
        return (
            Session.query(
                Question,
                func.coalesce(func.sum(Choice.votes), 0).label("total_votes"),
            )
            .outerjoin(Choice, Choice.question_id == Question.id)
            .group_by(Question.id)
            .order_by(func.coalesce(func.sum(Choice.votes), 0).desc())
            .all()
        )
