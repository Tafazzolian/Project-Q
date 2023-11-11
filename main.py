from fastapi.staticfiles import StaticFiles
from redis.asyncio import Redis
from config.configs import config
import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api import users,files,shops,admin
from app.middlewares.Authentication import AuthenticateMiddleware
from app.middlewares.Header_security import HeaderSecurityMiddleware
from app.middlewares.Rate_limiter import RateLimiter
from config.logs import logger
from contextlib import asynccontextmanager


#----------------------redis connection and jobs----------------
@asynccontextmanager
async def lifespan(app:FastAPI):
    redis_host: str=config.REDIS_HOST
    redis_port: int=config.REDIS_PORT
    redis_db: int = 0
    r = await Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True,retry_on_timeout=True)
    app.state.redis = r
    try:
        yield
    finally:
        await app.state.redis.close()
    #image/file processing worker in redis    
    # while True:
    #     job_data_json = r.brpop('file_queue')[1]
    #     job_data = json.loads(job_data_json)
    #     process_file(job_data)


#----------------------routers and app------------------------
app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(shops.router)
app.include_router(files.router)
app.include_router(admin.router)


#----------------------error logging--------------------------
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logger.exception("An unexpected error occurred: %s" % str(exc))
    logger.debug(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

#----------------------middlewares----------------------------
app.add_middleware(AuthenticateMiddleware)
app.add_middleware(HeaderSecurityMiddleware)
#app.add_middleware(RateLimiter)


#----------------------background tasks------------------------
from apscheduler.schedulers.background import BackgroundScheduler
from config.background_tasks import empty_log_cleaner

scheduler = BackgroundScheduler()
scheduler.add_job(empty_log_cleaner, 'interval', minutes = 2)#,hours=6 , max)
scheduler.start()
# logger.critical("Fire start")


#-------------------templates and static files-----------------
app.mount("/static", StaticFiles(directory="app/static"), name="static")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=config.PORT, reload=True)