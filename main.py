from fastapi import FastAPI
from app.api import user
from app.middlewares.Authentication import AuthenticateMiddleware
from app.middlewares.Header_security import HeaderSecurityMiddleware
from app.middlewares.Rate_limiter import RateLimiter

app = FastAPI()

app.add_middleware(AuthenticateMiddleware)
app.add_middleware(HeaderSecurityMiddleware)
app.add_middleware(RateLimiter)



app.include_router(user.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host="0.0.0.0", port=8090, reload=True)