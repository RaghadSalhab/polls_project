# polls/cache_decorator.py
from functools import wraps
from .cache import get_cache, set_cache
import logging

logger = logging.getLogger('polls_logger')

def cache_response(key_func, expire: int = 300, show_emoji: bool = True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = key_func(*args, **kwargs)
            cached_data = get_cache(cache_key)
            if cached_data is not None:
                msg = f"Cache hit for {cache_key}"
                if show_emoji:
                    msg = "📦 " + msg
                logger.info(msg)
                logger.info(f"{'✅ Returning cached result' if show_emoji else 'Returning cached result'} for {cache_key}")
                return cached_data
            result = func(*args, **kwargs)
            if result is not None:
                set_cache(cache_key, result, expire=expire)
            return result
        return wrapper
    return decorator
