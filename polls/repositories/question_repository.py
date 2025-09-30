from sqlalchemy.orm import joinedload
from polls.models.database import Session
from polls.models.question import Question
from polls.models.choice import Choice

class QuestionRepository:

    @staticmethod
    def list_questions(search: str = None):
        query = Session.query(Question).options(joinedload(Question.choices))
        if search:
            query = query.filter(Question.question_text.ilike(f"%{search}%"))
        return query.all()

    @staticmethod
    def list_questions_for_user(user_id: int):
        questions = Session.query(Question)\
                           .filter(Question.created_by_id == user_id)\
                           .all()
        print(f"Found {len(questions)} questions for user {user_id}")
        return questions

    @staticmethod
    def get_question(question_id: int):
        return Session.query(Question)\
                      .options(joinedload(Question.created_by), joinedload(Question.choices))\
                      .filter(Question.id == question_id)\
                      .first()

    @staticmethod
    def create_question(user_id: int, question_text: str, choices: list[str] = None):
        question = Question(created_by_id=user_id, question_text=question_text)
        Session.add(question)
        Session.flush()  

        if choices:
            for choice_text in choices:
                choice = Choice(question_id=question.id, choice_text=choice_text, votes=0)
                Session.add(choice)

        Session.commit()
        Session.refresh(question)
        return question

    @staticmethod
    def update_question(question_id: int, question_text: str, choices: list[dict] = None):
        question = Session.query(Question)\
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
                    Session.add(new_choice)

        Session.commit()
        Session.refresh(question)
        return question

    @staticmethod
    def delete_question(question_id: int):
        question = Session.query(Question).filter(Question.id == question_id).first()
        if question:
            Session.delete(question)
            Session.commit()
