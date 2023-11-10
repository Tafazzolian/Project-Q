from sqlalchemy.orm import Session
from db.models.shop import Shop
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request, status
from sqlalchemy import delete, or_, text

from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.cache import cache


class ShopRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_shop(self,user_data):
        conditions = []
        if "id" in user_data:
            conditions.append(Shop.id      == user_data["id"])
        if "user_id" in user_data:
            conditions.append(Shop.user_id       == user_data["user_id"])
        if "shop_name" in user_data:
            conditions.append(Shop.shop_name    == user_data["shop_name"])
        if "email" in user_data:
            conditions.append(Shop.email     == user_data["email"])
        if "phone" in user_data:
            conditions.append(Shop.phone == user_data["phone"])
        
        if not conditions:
            return None
        
        async with self.db:
            result = await self.db.execute(
            select(Shop).filter(or_(*conditions)))#.options(selectinload(User.relationships)))
            user = result.scalars().first()

        return user
    
    @cache(key="get_all_shops")
    async def get_all_shops(self, request:Request):
        async with self.db:
            result = await self.db.execute(
            select(Shop))
            users = result.scalars().all()
        return  users