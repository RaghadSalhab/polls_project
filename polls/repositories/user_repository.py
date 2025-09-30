from werkzeug.security import generate_password_hash
from polls.models.user import User
from polls.models.database import Session

class UserRepository:

    @staticmethod
    def get_user_by_id(user_id: int):
        return Session.get(User, user_id)

    @staticmethod
    def list_users():
        return Session.query(User).all()

    @staticmethod
    def create_user(username: str, email: str, password: str, is_superuser: bool = False):
        user = User(
            username=username,
            email=email,
            password=password,
            is_superuser=is_superuser,
            is_active=True
        )
        Session.add(user)
        Session.flush() 
        Session.refresh(user)
        return user

    @staticmethod
    def update_user(user_id: int, **kwargs):
        user = Session.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        for attr, value in kwargs.items():
            if attr == "password":
                value = generate_password_hash(value)
            setattr(user, attr, value)
        Session.flush()
        Session.refresh(user)
        return user

    @staticmethod
    def delete_user(user_id: int):
        user = Session.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        Session.delete(user)
        return True
