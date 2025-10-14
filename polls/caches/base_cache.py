# polls/caches/base_cache.py
import json
from .redis_client import RedisClient

class BaseCache:
    def __init__(self):
        self.client = RedisClient.get_client()

    def get(self, key):
        value = self.client.get(key)
        if value is None:
            print(f"❌ [MISS] Cache miss for key '{key}'")
            return None
        try:
            value = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            pass
        print(f"✅ [HIT] Cache hit for key '{key}'")
        return value

    def set(self, key, value, expire=None):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        self.client.set(key, value, ex=expire)
        print(f"✅ Cache set for key '{key}'")

    def delete(self, key):
        self.client.delete(key)
        print(f"🗑️ Cache deleted for key '{key}'")
