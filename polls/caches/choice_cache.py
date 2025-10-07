# polls/caches/choice_cache.py
from .base_cache import BaseCache

class ChoiceCache(BaseCache):
    name = "choice"

    def get_by_id(self, choice_id: int):
        key = f"{self.name}:{choice_id}"
        return self.get(key)

    def set_by_id(self, choice_id: int, value, expire=None):
        key = f"{self.name}:{choice_id}"
        self.set(key, value, expire=expire)

    def delete_by_id(self, choice_id: int):
        key = f"{self.name}:{choice_id}"
        self.delete(key)

    def get_list_for_question(self, question_id: int):
        key = f"choices:list:{question_id}"
        return self.get(key)

    def set_list_for_question(self, question_id: int, value, expire=None):
        key = f"choices:list:{question_id}"
        self.set(key, value, expire=expire)

    def delete_list_for_question(self, question_id: int):
        key = f"choices:list:{question_id}"
        self.delete(key)
