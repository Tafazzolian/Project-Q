from fastapi import FastAPI
from app.api import user
from app.middlewares.Authentication import AuthenticateMiddleware

app = FastAPI()
app.add_middleware(AuthenticateMiddleware)
app.include_router(user.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host="0.0.0.0", port=8090, reload=True)