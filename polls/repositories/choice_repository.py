from sqlalchemy.orm import joinedload
from polls.models.choice import Choice
from polls.models.database import Session
from polls.repositories.base_repository import BaseRepository

class ChoiceRepository(BaseRepository):
    model = Choice

    @classmethod
    def list_choices_for_question(cls, question_id: int):
        return Session.query(cls.model).filter(cls.model.question_id == question_id).all()

    @classmethod
    def get_with_question(cls, choice_id: int):
        """Get choice with its related question"""
        return (
            Session.query(cls.model)
            .options(joinedload(cls.model.question))
            .filter(cls.model.id == choice_id)
            .first()
        )

    @classmethod
    def vote(cls, choice_id: int):
        choice = cls.get(choice_id)
        if not choice:
            return None
        choice.votes += 1
        Session.flush()
        Session.refresh(choice)
        return choice
