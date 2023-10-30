from fastapi import Depends
from app.repositories.user_repo import UserRepository
from app.services.user_services import UserService
from typing import Any, Optional
from sqlalchemy.orm import Session
from fastapi.params import Query
from starlette.requests import Request
from config.Auth import AccessToken
from utils.tools import Tools

from db import models
from database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def inject_session_to_repo(db: Session = Depends(get_db)) -> UserRepository:
    """
    Provides an instance of UserRepository to be used as a dependency.
    """
    return UserRepository(db)


def get_user_service(repo: UserRepository = Depends(inject_session_to_repo)) -> UserService:
    return UserService(repo)


def get_current_user(request: Request, token: Optional[str] = None):
    if not token:
        token = request.state.token
    user_id = AccessToken().check_token(token)
    return user_id
    

def already_logged_in_check(request:Request):
    if not request.state.token:
        Tools.yellow(key="login_check:",text="no tokens found")
        return None
    else:
        user_id = get_current_user(request=request, token = request.state.token)
        if user_id:
            Tools.green(key="login_check:",text="token approved")
            return user_id
        else:
            Tools.red(key="login_check:",text="token failed")
            None


# def current_user(request: Request):
#     if request.state.user is None:
#         raise ValidationException()
#     return request.state.user