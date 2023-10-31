from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi.util import get_remote_address
import redis.asyncio as redis
from utils.tools import Tools
from config.configs import config
from config.logs import logger

class RateLimiter(BaseHTTPMiddleware):
    redis_host: str=config.REDIS_HOST
    redis_port: int=config.REDIS_PORT
    redis_db: int = 0

    async def dispatch(self, request: Request, call_next):
        r = redis.Redis(host=self.redis_host, port=self.redis_port, db=self.redis_db, decode_responses=True,retry_on_timeout=True)
        Tools.green(key="Rate_limiter_middleware:",text="Rate-limiter middleware started.")
        client_ip = get_remote_address(request)
        limit = 10  # 10 requests
        interval = 60  # per 60 seconds
        try:
            count = await r.get(client_ip)
            Tools.green(text="Redis connection success")
        
            if count is not None:
                count = int(count)
                if count >= limit: 
                    return JSONResponse(content={"request_limit":"Rate limit exceeded"}, status_code=429)
            else:
                count = 0

            pipeline = r.pipeline()
            pipeline.incr(client_ip)
            if count == 0:
                pipeline.expire(client_ip, interval)
            await pipeline.execute()

            response = await call_next(request)
            return response
        except:
            logger.exception("<red>Redis connection failed</red>")
            response = await call_next(request)
            return response