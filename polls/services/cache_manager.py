import redis
import json
from polls.utils.logger import logger
import threading

class CacheManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host='127.0.0.1', port=6379, db=0, default_expire=300):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self.r = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
            socket_timeout=5
        )
        self.default_expire = default_expire
        self._initialized = True

    # ===== Helper =====
    def _is_cache_valid(self, cached, ttl):
        return cached is not None and ttl not in (None, -2)

    # ===== Core Methods =====
    def get(self, key):
        try:
            cached = self.r.get(key)
            ttl = self.r.ttl(key)
        except Exception as e:
            logger.error(f"⚠️ Redis get failed for {key}: {e}")
            return None

        if not self._is_cache_valid(cached, ttl):
            print(f"❌ Cache miss for {key}")  
            return None

        try:
            data = json.loads(cached)
        except Exception:
            data = cached

        ttl_msg = "♾️ No expiry set" if ttl == -1 else f"⏱️ Expires in {ttl}s"
        print(f"📦 Cache hit for {key} ({ttl_msg})")  
        return data

    def set(self, key, value, expire=None):
        expire = expire or self.default_expire
        try:
            serialized = json.dumps(value, default=str)
            self.r.set(key, serialized, ex=expire)
            return True
        except Exception as e:
            logger.error(f"⚠️ Failed to set cache for {key}: {e}")
            return False

    def delete(self, key):
        try:
            self.r.delete(key)
        except Exception as e:
            logger.error(f"⚠️ Failed to delete cache for {key}: {e}")


# ===== Global function for convenience =====
_cache_manager_instance = None

def get_cache_manager():
    global _cache_manager_instance
    if _cache_manager_instance is None:
        _cache_manager_instance = CacheManager()
    return _cache_manager_instance
