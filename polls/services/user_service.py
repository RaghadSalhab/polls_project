from polls.repositories.user_repository import UserRepository
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

class UserService:

    @staticmethod
    def get_user(user_id):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise ObjectDoesNotExist("User not found")
        return user

    @staticmethod
    def list_users():
        return UserRepository.list_users()

    @staticmethod
    def create_user(username, email, password):
        return UserRepository.create_user(username, email, password)

    @staticmethod
    def update_user(requesting_user, user_id, **kwargs):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise ObjectDoesNotExist("User not found")

        if requesting_user != user:
            raise PermissionDenied("You cannot edit this user")

        return UserRepository.update_user(user_id, **kwargs)

    @staticmethod
    def delete_user(requesting_user, user_id):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise ObjectDoesNotExist("User not found")

        if requesting_user != user and not requesting_user.is_superuser:
            raise PermissionDenied("You cannot delete this user")

        UserRepository.delete_user(user_id)
