# polls/services/user_service.py
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from polls.repositories.user_repository import UserRepository
from polls.schemas.user import UserSchema
from polls.services.cache_manager import get_cache_manager

class UserService:
    cache = get_cache_manager()

    @staticmethod
    def get_user(user_id: int):
        cache_key = f"user:{user_id}"
        cached_data = UserService.cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise ObjectDoesNotExist("User not found")

        data = UserSchema().dump(user)
        UserService.cache.set(cache_key, data, expire=300)
        return data

    @staticmethod
    def list_users():
        cache_key = "users:list"
        cached_data = UserService.cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        users = UserRepository.list_users()
        data = UserSchema(many=True).dump(users)
        UserService.cache.set(cache_key, data, expire=300)
        return data

    @staticmethod
    def create_user(username: str, email: str, password: str):
        user = UserRepository.create_user(username, email, password)

        UserService.cache.delete("users:list")
        return UserSchema().dump(user)

    @staticmethod
    def update_user(requesting_user, user_id: int, **kwargs):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise ObjectDoesNotExist("User not found")
        if requesting_user.id != user.id:
            raise PermissionDenied("You cannot edit this user")

        user = UserRepository.update_user(user_id, **kwargs)
        data = UserSchema().dump(user)

        UserService.cache.set(f"user:{user_id}", data, expire=300)
        UserService.cache.delete("users:list")
        return data

    @staticmethod
    def delete_user(requesting_user, user_id: int):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise ObjectDoesNotExist("User not found")
        if requesting_user.id != user.id and not getattr(requesting_user, "is_superuser", False):
            raise PermissionDenied("You cannot delete this user")

        UserRepository.delete_user(user_id)

        UserService.cache.delete(f"user:{user_id}")
        UserService.cache.delete("users:list")
