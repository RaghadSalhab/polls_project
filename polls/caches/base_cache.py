import json
import redis

class BaseCache:
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379, db=0)

    def get(self, key):
        value = self.client.get(key)
        if value is None:
            print(f"❌ Cache miss for {key}")
            return None
        try:
            value = json.loads(value)  # تحويل من string لـ dict/list
        except json.JSONDecodeError:
            pass
        print(f"✅ Cache hit for {key}")
        return value

    def set(self, key, value, expire=None):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)  # تحويل dict/list لـ string
        self.client.set(key, value, ex=expire)
        print(f"✅ Cache set for {key}")

    def delete(self, key):
        self.client.delete(key)
        print(f"🗑️ Cache deleted for {key}")
