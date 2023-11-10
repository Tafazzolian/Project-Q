from sqlalchemy.orm import Session
from db.models.ufo import Ufo
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request, status
from sqlalchemy import delete, or_, text

from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.cache import cache


class UfoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_ufo(self,user_data):
        conditions = []
        if "id" in user_data:
            conditions.append(Ufo.id        == user_data["id"])
        if "tax" in user_data:
            conditions.append(Ufo.tax_number    == user_data["tax"])
        if "national_code" in user_data:
            conditions.append(Ufo.national_code     == user_data["national_code"])
        if "shaba" in user_data:
            conditions.append(Ufo.Shaba_number == user_data["shaba"])
        
        if not conditions:
            return None
        
        async with self.db:
            result = await self.db.execute(
            select(Ufo).filter(or_(*conditions)))#.options(selectinload(User.relationships)))
            user = result.scalars().first()

        return user
    
    @cache(key="get_all_ufos")
    async def get_all_ufos(self, request:Request):
        async with self.db:
            result = await self.db.execute(
            select(Ufo))
            users = result.scalars().all()
        return  users