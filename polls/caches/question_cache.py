# polls/caches/question_cache.py
from .base_cache import BaseCache

class QuestionCache(BaseCache):
    name = "question"

    def get_by_id(self, question_id: int):
        key = f"{self.name}:{question_id}"
        return self.get(key)

    def set_by_id(self, question_id: int, value, expire=None):
        key = f"{self.name}:{question_id}"
        self.set(key, value, expire=expire)

    def delete_by_id(self, question_id: int):
        key = f"{self.name}:{question_id}"
        self.delete(key)

    def get_list(self, search: str = None):
        key = f"{self.name}:list:{search or 'all'}"
        return self.get(key)

    def set_list(self, value, search: str = None, expire=None):
        key = f"{self.name}:list:{search or 'all'}"
        self.set(key, value, expire=expire)

    def delete_list(self, search: str = None):
        key = f"{self.name}:list:{search or 'all'}"
        self.delete(key)
