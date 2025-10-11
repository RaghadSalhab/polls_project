import redis
import json

class BaseCache:
    _clients = {}  

    def __init__(self, client_name: str = "default_cache_client"):
        self.client_name = client_name
        if client_name in BaseCache._clients:
            self.client = BaseCache._clients[client_name]
        else:
            self.client = redis.Redis(
                host='localhost',
                port=6380,
                db=0,
                client_name=client_name
            )
            BaseCache._clients[client_name] = self.client
            print(f"🔌 New Redis client created: {client_name}")

    def get(self, key):
        value = self.client.get(key)
        if value is None:
            print(f"❌ Cache miss for {key} (client: {self.client_name})")
            return None
        try:
            value = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            pass
        print(f"✅ Cache hit for {key} (client: {self.client_name})")
        return value

    def set(self, key, value, expire=None):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        self.client.set(key, value, ex=expire)
        print(f"✅ Cache set for {key} (client: {self.client_name})")

    def delete(self, key):
        self.client.delete(key)
        print(f"🗑️ Cache deleted for {key} (client: {self.client_name})")
