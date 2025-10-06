from polls.repositories.user_repository import UserRepository
from polls.schemas.user import UserSchema
from polls.services.redis_client import r
from polls.cache import get_cache, set_cache
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

class UserService:

    @staticmethod
    def get_user(user_id: int):
        cache_key = f"user:{user_id}"
        cached_data = get_cache(cache_key)
        if cached_data:
            return cached_data

        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise ObjectDoesNotExist("User not found")

        data = UserSchema().dump(user)
        set_cache(cache_key, data, expire=300)
        return data

    @staticmethod
    def list_users():
        cache_key = "users:list"
        cached_data = get_cache(cache_key)
        if cached_data:
            return cached_data

        users = UserRepository.list_users()
        data = UserSchema(many=True).dump(users)
        set_cache(cache_key, data, expire=300)
        return data

    @staticmethod
    def create_user(username: str, email: str, password: str):
        user = UserRepository.create_user(username, email, password)
        r.delete("users:list") 
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

        set_cache(f"user:{user_id}", data, expire=300)
        r.delete("users:list")
        return data

    @staticmethod
    def delete_user(requesting_user, user_id: int):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise ObjectDoesNotExist("User not found")
        if requesting_user.id != user.id and not getattr(requesting_user, "is_superuser", False):
            raise PermissionDenied("You cannot delete this user")

        UserRepository.delete_user(user_id)
        r.delete(f"user:{user_id}")
        r.delete("users:list")
