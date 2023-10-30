from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi.util import get_remote_address
import redis.asyncio as redis
from time import sleep
from utils.tools import Tools

redis_connection_retry = 0
while redis_connection_retry < 5:
    try:
        r = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True,retry_on_timeout=True)
        Tools.green(key="Rate_limiter_middleware:",text='Connection to Redis established')
        break
    except:
        sleep(1)
        redis_connection_retry += 1
# else:
#     r.close()
#     raise ConnectionError('Failed to connect to Redis after 10 retries.')

class RateLimiter(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        Tools.green(key="Rate_limiter_middleware:",text="Rate-limiter middleware started.")
        client_ip = get_remote_address(request)
        limit = 10  # 10 requests
        interval = 60  # per 60 seconds

        count = await r.get(client_ip)
        if count is not None:
            count = int(count)
            if count >= limit: 
                return JSONResponse(content={"request_limit":"Rate limit exceeded"}, status_code=429)
        else:
            count = 0

        # Increment the count and set the expiration time if necessary
        pipeline = r.pipeline()
        pipeline.incr(client_ip)
        if count == 0:
            pipeline.expire(client_ip, interval)
        await pipeline.execute()

        response = await call_next(request)
        return response