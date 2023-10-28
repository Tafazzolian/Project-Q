from fastapi import Depends, FastAPI
from fastapi.exceptions import ValidationException
from app.repositories.user_repo import UserRepository
from app.services.user_services import UserService
from typing import Any
from sqlalchemy.orm import Session
from fastapi.params import Query
from sqlalchemy import desc
from starlette.requests import Request

from db import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def current_user(request: Request):
    if request.state.user is None:
        raise ValidationException()
    return request.state.user

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """
    Provides an instance of UserRepository to be used as a dependency.
    """
    return UserRepository(db)

def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)