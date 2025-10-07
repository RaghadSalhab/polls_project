# polls/caches/user_cache.py
from .base_cache import BaseCache

class UserCache(BaseCache):
    name = "user"

    def get_by_id(self, user_id: int):
        key = f"{self.name}:{user_id}"
        return self.get(key)

    def set_by_id(self, user_id: int, value, expire=None):
        key = f"{self.name}:{user_id}"
        self.set(key, value, expire=expire)

    def delete_by_id(self, user_id: int):
        key = f"{self.name}:{user_id}"
        self.delete(key)

    def get_list(self):
        key = f"{self.name}:list"
        return self.get(key)

    def set_list(self, value, expire=None):
        key = f"{self.name}:list"
        self.set(key, value, expire=expire)

    def delete_list(self):
        key = f"{self.name}:list"
        self.delete(key)
