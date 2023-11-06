from datetime import datetime
import json
from diskcache import Cache
from functools import wraps

def as_dict(data):
    if isinstance(data, list):
        return [as_dict(item) for item in data]
    return {
        c.name: getattr(data, c.name).isoformat() if isinstance(getattr(data, c.name), datetime) else getattr(data, c.name)
        for c in data.__table__.columns
    }


def cache(key: str, expire: int = 60):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs["request"]
            redis = request.app.state.redis
            cached_value = await redis.get(key)
            if cached_value:
                print("cache worked")
                return json.loads(cached_value)

            # Call the decorated function
            result = await func(*args, **kwargs)
            result_dict = as_dict(result) if not isinstance(result, dict) else result

            # Set the result in the cache
            await redis.set(key, json.dumps(result_dict), ex=expire)
            return result

        return wrapper
    return decorator

    
# from config.logs import cache_logger

#cache = Cache(directory='/Users/tafazzolian/Documents/Q-Pay/debug_cache/')

# cache.stats(enable=True)
# hits, misses = cache.stats()

# cache_logger.critical(f'Cache Hits: {hits}, Cache Misses: {misses}')

# async def cache_func(key, data):
#     if key in cache:
#         return cache[key]
#     else:
#         result = await data()
#         cache[key] = result
#         return result
