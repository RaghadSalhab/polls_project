from .base_cache import BaseCache

class StatsCache(BaseCache):
    name = "stats"

    def get_top_question(self):
        key = f"{self.name}:top_question"
        return self.get(key)

    def set_top_question(self, value, expire=None):
        key = f"{self.name}:top_question"
        self.set(key, value, expire=expire)

    def get_question_votes(self, question_id: int):
        key = f"{self.name}:question_votes:{question_id}"
        return self.get(key)

    def set_question_votes(self, question_id: int, value, expire=None):
        key = f"{self.name}:question_votes:{question_id}"
        self.set(key, value, expire=expire)

    def get_top_choice(self):
        key = f"{self.name}:top_choice"
        return self.get(key)

    def set_top_choice(self, value, expire=None):
        key = f"{self.name}:top_choice"
        self.set(key, value, expire=expire)

    def get_questions_with_votes(self):
        key = f"{self.name}:questions_with_votes"
        return self.get(key)

    def set_questions_with_votes(self, value, expire=None):
        key = f"{self.name}:questions_with_votes"
        self.set(key, value, expire=expire)
