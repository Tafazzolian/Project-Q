from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi.util import get_remote_address
from utils.tools import Tools
from config.logs import logger
from redis.exceptions import ConnectionError

class RateLimiter(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next):
        redis = request.app.state.redis
        
        Tools.green(key="Rate_limiter_middleware:",text="Rate-limiter middleware started.")
        client_ip = get_remote_address(request)
        limit = 2      # 10 requests
        interval = 60  # per 60 seconds
        try:
            if redis.get(client_ip):
                count = redis.get(client_ip)
                Tools.green(text="Redis connection success")
                count = int(count)
                if count >= limit: 
                    return JSONResponse(content={"request_limit":"Rate limit exceeded"}, status_code=429)
            else:
                count = 0

            pipeline = redis.pipeline()
            pipeline.incr(client_ip)
            if count == 0:
                pipeline.expire(client_ip, interval)
            pipeline.execute()

            response = await call_next(request)
            return response

        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            response = await call_next(request)
            return response
            logger.exception("<red>Redis connection failed</red>")
            response = await call_next(request)
            return response