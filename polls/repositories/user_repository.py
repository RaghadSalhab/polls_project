# repositories/user_repository.py
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from polls.models.user import User
from polls.models.database import SessionLocal

class UserRepository:

    @staticmethod
    def get_user_by_id(user_id: int):
        with SessionLocal() as session:
            return session.get(User, user_id)

    @staticmethod
    def list_users():
        with SessionLocal() as session:
            return session.query(User).all()


    @staticmethod
    def create_user(username: str, email: str, password: str, is_superuser: bool = False):
        hashed_password = generate_password_hash(password)
        user = User(
            username=username,
            email=email,
            password=hashed_password,
            is_superuser=is_superuser,
            is_active=True
        )

        with SessionLocal() as session:
            session.add(user)
            session.commit()  
            session.refresh(user)
            return user

    @staticmethod
    def update_user(user_id: int, **kwargs):
        with SessionLocal() as session:
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
    def delete_user(user_id: int):
        with SessionLocal() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            session.delete(user)
            session.commit()
            return True
