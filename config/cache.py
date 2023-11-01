from diskcache import Cache
from config.logs import cache_logger

cache = Cache(directory='/Users/tafazzolian/Documents/Q-Pay/debug_cache/')
cache.stats(enable=True)
hits, misses = cache.stats()

cache_logger.info(f'Cache Hits: {hits}, Cache Misses: {misses}')

async def cache_func(key, data):
    if key in cache:
        return cache[key]
    else:
        result = await data()
        cache[key] = result
        return result
