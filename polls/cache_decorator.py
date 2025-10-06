# polls/cache_decorator.py
from functools import wraps
from .cache import get_cache, set_cache

def cache_response(key_func, expire: int = 300):
    """
    Decorator for caching function results in Valkey.
    key_func: function that takes same args as decorated func and returns a cache key string.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = key_func(*args, **kwargs)
            cached_data = get_cache(cache_key)
            if cached_data is not None:
                return cached_data
            result = func(*args, **kwargs)
            if result is not None:
                set_cache(cache_key, result, expire=expire)
            return result
        return wrapper
    return decorator
