# polls/services/user_service.py
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from polls.repositories.user_repository import UserRepository
from polls.schemas.user import UserSchema
from polls.caches.user_cache import UserCache
from ddtrace import tracer

class UserService:

    cache = UserCache(client_name="user_cache_client")
    
    @classmethod
    def get_user(cls, user_id: int):
        with tracer.trace("user_service.get_user"):
            cached_data = cls.cache.get_by_id(user_id)
            if cached_data:
                return cached_data

            user = UserRepository.get(user_id)
            if not user:
                raise ObjectDoesNotExist("User not found")

            data = UserSchema().dump(user)
            cls.cache.set_by_id(user_id, data, expire=300)
            return data

    @classmethod
    def list_users(cls):
        with tracer.trace("user_service.list_users"):
            cached_data = cls.cache.get_list()
            if cached_data:
                return cached_data

            users = UserRepository.list_all()
            data = UserSchema(many=True).dump(users)
            cls.cache.set_list(data, expire=300)
            return data

    @classmethod
    def create_user(cls, username: str, email: str, password: str):
        with tracer.trace("user_service.create_user"):
            existing_user = UserRepository.get_by_username(username)
            if existing_user:
                raise ValueError("Username already exists")
            user = UserRepository.create_user(username, email, password)

            cls.cache.delete_list()
            return user
        
    @classmethod
    def update_user(cls, requesting_user, user_id: int, **kwargs):
        with tracer.trace("user_service.update_user"):
            user = UserRepository.get(user_id)
            if not user:
                raise ObjectDoesNotExist("User not found")
            if requesting_user.id != user.id:
                raise PermissionDenied("You cannot edit this user")

            user = UserRepository.update_user(user_id, **kwargs)
            data = UserSchema().dump(user)

            cls.cache.set_by_id(user_id, data, expire=300)
            cls.cache.delete_list()
            return data

    @classmethod
    def delete_user(cls, requesting_user, user_id: int):
        with tracer.trace("user_service.delete_user"):
            user = UserRepository.get(user_id)
            if not user:
                raise ObjectDoesNotExist("User not found")
            if requesting_user.id != user.id and not getattr(requesting_user, "is_superuser", False):
                raise PermissionDenied("You cannot delete this user")
            UserRepository.delete_by_id(user_id)
            cls.cache.delete_by_id(user_id)
            cls.cache.delete_list()

    @classmethod
    def get_profile(cls, user_id: int):
        cached_data = cls.cache.get_profile(user_id)
        if cached_data:
            return cached_data

        user = UserRepository.get(user_id)
        if not user:
            raise ObjectDoesNotExist("User not found")

        data = UserSchema().dump(user)
        cls.cache.set_profile(user_id, data, expire=300)
        return data

    @classmethod
    def update_profile(cls, requesting_user, **kwargs):
        user_id = requesting_user.id
        user = UserRepository.update_user(user_id, **kwargs)
        data = UserSchema().dump(user)
        cls.cache.set_profile(user_id, data, expire=300)
        cls.cache.delete_list()
        return data