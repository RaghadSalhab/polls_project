# models/question.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
from .user import User
from datetime import datetime


class Question(Base):
    __tablename__ = "polls_question"
    id = Column(Integer, primary_key=True)
    question_text = Column(String(200), nullable=False)
    pub_date = Column(DateTime, nullable=False, default=datetime.now)
    created_by_id = Column(Integer, ForeignKey("auth_user.id"), nullable=False)

    created_by = relationship("User", back_populates="questions")
    choices = relationship("Choice", back_populates="question", cascade="all, delete-orphan")

