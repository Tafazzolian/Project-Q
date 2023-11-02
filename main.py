from config.configs import config
import traceback
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from app.api import user
from app.middlewares.Authentication import AuthenticateMiddleware
from app.middlewares.Header_security import HeaderSecurityMiddleware
from app.middlewares.Rate_limiter import RateLimiter
from config.logs import logger

app = FastAPI()
app.include_router(user.router)

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    backgroundTasks = BackgroundTasks
    logger.exception("An unexpected error occurred")
    logger.debug(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

app.add_middleware(AuthenticateMiddleware)
app.add_middleware(HeaderSecurityMiddleware)
app.add_middleware(RateLimiter)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host="0.0.0.0", port=config.PORT, reload=True)