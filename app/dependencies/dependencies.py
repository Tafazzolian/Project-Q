from fastapi import Depends, HTTPException
from app.repositories.user_repo import UserRepository
from app.services.user_services import UserService
from typing import Any, Optional
from sqlalchemy.orm import Session
from fastapi.params import Query
from starlette.requests import Request
from config.authentication import AccessToken
from utils.tools import Tools

from db import models
from database import SessionLocal, engine, AsyncSessionLocal, async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as db:
        yield db

async def inject_session_to_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """
    Provides an instance of UserRepository to be used as a dependency.
    """
    return UserRepository(db)


def get_user_service(repo: UserRepository = Depends(inject_session_to_repo)) -> UserService:
    return UserService(repo)


async def get_current_user(request: Request, token: Optional[str] = None):
    if not token:
        token = request.state.token
    user_id = await AccessToken().check_token(token, request)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")

    return user_id


# def get_current_user(request: Request):
#     if request.state.user is None:
#         raise HTTPException(status_code=404,detail="user not found")
#     return request.state.user