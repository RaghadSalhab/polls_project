# polls/services/redis_client.py
import redis

r = redis.Redis(
    host='127.0.0.1',  
    port=6379,
    db=0,
    decode_responses=True,
    socket_timeout=5
)
