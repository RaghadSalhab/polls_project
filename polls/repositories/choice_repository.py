from sqlalchemy.orm import joinedload
from polls.models.choice import Choice
from polls.models.question import Question
from polls.models.database import Session

class ChoiceRepository:

    @staticmethod
    def list_choices_for_question(question_id: int):
        return Session.query(Choice).filter(Choice.question_id == question_id).all()

    @staticmethod
    def get_choice(choice_id: int):
        return (
            Session.query(Choice)
            .options(joinedload(Choice.question))
            .filter(Choice.id == choice_id)
            .first()
        )

    @staticmethod
    def create_choice(question_id: int, choice_text: str):
        question = Session.query(Question).filter(Question.id == question_id).first()
        if not question:
            return None
        choice = Choice(question_id=question.id, choice_text=choice_text)
        Session.add(choice)
        Session.flush()     
        Session.refresh(choice)  
        return choice

    @staticmethod
    def update_choice(choice_id: int, choice_text: str):
        choice = Session.query(Choice).filter(Choice.id == choice_id).first()
        if not choice:
            return None
        choice.choice_text = choice_text
        return choice

    @staticmethod
    def delete_choice(choice_id: int):
        choice = Session.query(Choice).filter(Choice.id == choice_id).first()
        if choice:
            Session.delete(choice)

    @staticmethod
    def vote(choice_id: int):
        choice = Session.query(Choice).filter(Choice.id == choice_id).first()
        if not choice:
            return None
        choice.votes += 1
        Session.flush()
        Session.refresh(choice)
        return choice
