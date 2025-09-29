# services/user_service.py
from polls.repositories.user_repository import UserRepository
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib.auth.hashers import make_password


class UserService:

    @staticmethod
    def get_user(user_id: int):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise ObjectDoesNotExist("User not found")
        return user

    @staticmethod
    def list_users():
        return UserRepository.list_users()

    @staticmethod
    def create_user(username: str, email: str, password: str):
        hashed_password = make_password(password)
        return UserRepository.create_user(username, email, hashed_password)

    @staticmethod
    def update_user(requesting_user, user_id: int, **kwargs):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise ObjectDoesNotExist("User not found")

        if requesting_user.id != user.id:
            raise PermissionDenied("You cannot edit this user")

        return UserRepository.update_user(user_id, **kwargs)

    @staticmethod
    def delete_user(requesting_user, user_id: int):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise ObjectDoesNotExist("User not found")

        if requesting_user.id != user.id and not getattr(requesting_user, "is_superuser", False):
            raise PermissionDenied("You cannot delete this user")

        UserRepository.delete_user(user_id)
