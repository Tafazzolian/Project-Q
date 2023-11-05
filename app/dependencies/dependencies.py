from fastapi import Depends
from app.repositories.user_repo import UserRepository
from app.services.user_services import UserService
from typing import Any, Optional
from sqlalchemy.orm import Session
from fastapi.params import Query
from starlette.requests import Request
from config.authentication import AccessToken
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
    user_id = AccessToken().check_token(token, request)
    return user_id


# def current_user(request: Request):
#     if request.state.user is None:
#         raise ValidationException()
#     return request.state.user