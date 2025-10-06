
# polls/cache.py
import redis

v = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)

def get_cache(key):
    cached = v.get(key)
    if cached:
        print(f"📦 Cache hit for {key}")
        try:
            import json
            return json.loads(cached)
        except Exception:
            return cached
    return None

def set_cache(key, value, expire: int = 300):
    import json
    v.set(key, json.dumps(value), ex=expire)
    print(f"💾 Cache set for {key} (expire={expire}s)")
