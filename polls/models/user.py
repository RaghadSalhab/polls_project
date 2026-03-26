# models/user.py
from sqlalchemy import Column, Integer, String, Boolean
from .database import Base  
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "auth_user"
    id = Column(Integer, primary_key=True)
    username = Column(String(150), nullable=False)
    email = Column(String(254))
    password = Column(String(128))
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    questions = relationship("Question", back_populates="created_by")
