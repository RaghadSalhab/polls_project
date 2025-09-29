# repositories/user_repository.py
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from polls.models.user import User
from polls.models.database import SessionLocal

class UserRepository:

    @staticmethod
    def get_user_by_id(session, user_id: int):
        return session.get(User, user_id)

    @staticmethod
    def list_users(session):
        return session.query(User).all()

    @staticmethod
    def create_user(session, username: str, email: str, password: str, is_superuser: bool = False):
        user = User(
            username=username,
            email=email,
            password=password,
            is_superuser=is_superuser,
            is_active=True
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def update_user(session, user_id: int, **kwargs):
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        for attr, value in kwargs.items():
            if attr == "password":
                value = generate_password_hash(value)
            setattr(user, attr, value)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def delete_user(session, user_id: int):
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        session.delete(user)
        session.commit()
        return True
