from django.contrib.auth.hashers import make_password
from polls.models.user import User
from polls.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository):
    model = User  

    @classmethod
    def create_user(cls, username: str, email: str, password: str, is_superuser: bool = False, commit: bool = False):
        user = cls.model(
            username=username,
            email=email,
            password=make_password(password),
            is_superuser=is_superuser,
            is_active=True
        )
        return cls.add(user, commit=commit)

    @classmethod
    def update_user(cls, user_id: int, commit: bool = False, **kwargs):
        user = cls.get(user_id)
        if not user:
            return None
        for attr, value in kwargs.items():
            if attr == "password":
                value = make_password(value)
            setattr(user, attr, value)
        cls.flush()
        if commit:
            cls.commit()
        return user
