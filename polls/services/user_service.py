# polls/services/user_service.py
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from polls.repositories.user_repository import UserRepository
from polls.schemas.user import UserSchema
from polls.services.cache_manager import get_cache_manager

class UserService:
    cache = get_cache_manager()

    @classmethod
    def get_user(cls, user_id: int):
        cache_key = f"user:{user_id}"
        cached_data = cls.cache.get(cache_key)
        if cached_data:
            return cached_data

        user = UserRepository.get(user_id)
        if not user:
            raise ObjectDoesNotExist("User not found")

        data = UserSchema().dump(user)
        cls.cache.set(cache_key, data, expire=300)
        return data

    @classmethod
    def list_users(cls):
        cache_key = "users:list"
        cached_data = cls.cache.get(cache_key)
        if cached_data:
            return cached_data

        users = UserRepository.list_all()
        data = UserSchema(many=True).dump(users)
        cls.cache.set(cache_key, data, expire=300)
        return data

    @classmethod
    def create_user(cls, username: str, email: str, password: str):
        user = UserRepository.create_user(username, email, password)
        cls.cache.delete("users:list")
        return UserSchema().dump(user)

    @classmethod
    def update_user(cls, requesting_user, user_id: int, **kwargs):
        user = UserRepository.get(user_id)
        if not user:
            raise ObjectDoesNotExist("User not found")
        if requesting_user.id != user.id:
            raise PermissionDenied("You cannot edit this user")

        user = UserRepository.update_user(user_id, **kwargs)
        data = UserSchema().dump(user)

        cls.cache.set(f"user:{user_id}", data, expire=300)
        cls.cache.delete("users:list")
        return data

    @classmethod
    def delete_user(cls, requesting_user, user_id: int):
        user = UserRepository.get(user_id)
        if not user:
            raise ObjectDoesNotExist("User not found")
        if requesting_user.id != user.id and not getattr(requesting_user, "is_superuser", False):
            raise PermissionDenied("You cannot delete this user")

        UserRepository.delete_user_by_id(user_id)

        cls.cache.delete(f"user:{user_id}")
        cls.cache.delete("users:list")
