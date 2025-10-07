# polls/services/redis_client.py
import redis
import json
from polls.utils.logger import logger

# Redis client
r = redis.Redis(
    host='127.0.0.1',  
    port=6379,
    db=0,
    decode_responses=True,
    socket_timeout=5
)

def get_cache(key):
    """
    Retrieve value from Redis cache if exists.
    Returns Python object (decoded from JSON) or None if miss/expired.
    """
    try:
        pipe = r.pipeline()
        pipe.get(key)
        pipe.ttl(key)
        cached, ttl = pipe.execute()
    except Exception as e:
        logger.error(f"⚠️ Redis get failed for {key}: {e}")
        return None

    if cached is None or ttl == -2:
        logger.info(f"❌ Cache miss for {key}")
        return None

    try:
        data = json.loads(cached)
    except Exception:
        data = cached

    ttl_msg = "♾️ No expiry set" if ttl == -1 else f"⏱️ Expires in {ttl}s"
    logger.info(f"📦 Cache hit for {key} ({ttl_msg})")
    return data


def set_cache(key, value, expire: int = 300):
    """
    Set a value in Redis cache. Overwrites existing key.
    Returns True if set, False if failed.
    """
    try:
        # SET value with expiry
        r.set(key, json.dumps(value), ex=expire)
        logger.info(f"💾 Cache set for {key} (expire={expire}s)")
        return True
    except Exception as e:
        logger.error(f"⚠️ Failed to set cache for {key}: {e}")
        return False
