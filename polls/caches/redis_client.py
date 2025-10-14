# polls/caches/redis_client.py
import os
import redis
from threading import Lock

class RedisClient:
    _pool = None
    _lock = Lock()
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            with cls._lock:
                if cls._client is None:
                    host = os.getenv("REDIS_HOST", "localhost")
                    port = int(os.getenv("REDIS_PORT", 6379))
                    db = int(os.getenv("REDIS_DB", 0))
                    max_connections = int(os.getenv("REDIS_MAX_CONNECTIONS", 50))

                    cls._pool = redis.ConnectionPool(
                        host=host,
                        port=port,
                        db=db,
                        max_connections=max_connections,
                        decode_responses=True
                    )
                    cls._client = redis.Redis(connection_pool=cls._pool)
                    print(f"🔌 Redis client created: {host}:{port} db={db} pool_max={max_connections}")
        return cls._client

    @classmethod
    def get_pool_info(cls):
        return {
            "pool": cls._pool,
            "client": cls._client
        }
