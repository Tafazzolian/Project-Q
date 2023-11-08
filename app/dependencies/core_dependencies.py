from typing import Callable, Type
from fastapi import Depends
from utils.tools import Tools

from db import models
from database import SessionLocal, AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

class BaseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as db:
        yield db

def get_repo_dependency(repo_type: Type[BaseRepository]) -> Callable:
    async def dependency(db: AsyncSession = Depends(get_db)) -> BaseRepository:
        return repo_type(db)
    return dependency