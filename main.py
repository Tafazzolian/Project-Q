import redis
from config.configs import config
import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api import user
from app.middlewares.Authentication import AuthenticateMiddleware
from app.middlewares.Header_security import HeaderSecurityMiddleware
from app.middlewares.Rate_limiter import RateLimiter
from config.logs import logger
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app:FastAPI):
    redis_host: str=config.REDIS_HOST
    redis_port: int=config.REDIS_PORT
    redis_db: int = 0
    r = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True,retry_on_timeout=True)
    app.state.redis = r
    try:
        yield
    finally:
        await r.close()

app = FastAPI(lifespan=lifespan)

app.include_router(user.router)

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logger.exception("An unexpected error occurred: %s" % str(exc))
    logger.debug(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

app.add_middleware(AuthenticateMiddleware)
app.add_middleware(HeaderSecurityMiddleware)
app.add_middleware(RateLimiter)

#----------------------background tasks
from apscheduler.schedulers.background import BackgroundScheduler
from config.background_tasks import empty_log_cleaner

scheduler = BackgroundScheduler()
scheduler.add_job(empty_log_cleaner, 'interval', minutes = 2)#,hours=6 , max)
scheduler.start()
# logger.critical("Fire start")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host="0.0.0.0", port=config.PORT, reload=True)