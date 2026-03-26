# models/choice.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from .question import Question

class Choice(Base):
    __tablename__ = "polls_choice"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("polls_question.id"), nullable=False)
    choice_text = Column(String(200), nullable=False)
    votes = Column(Integer, default=0, nullable=False)

    question = relationship("Question", back_populates="choices")
