from polls.repositories.user_repository import UserRepository
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

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
        return UserRepository.create_user(username, email, password)

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
