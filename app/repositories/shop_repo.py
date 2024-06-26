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
            conditions.append(Shop.user_id == user_data["user_id"])
        if "shop_name" in user_data:
            conditions.append(Shop.shop_name    == user_data["shop_name"])
        if "email" in user_data:
            conditions.append(Shop.email   == user_data["email"])
        if "phone" in user_data:
            conditions.append(Shop.phone == user_data["phone"])
        
        if not conditions:
            return None
        
        async with self.db:
            result = await self.db.execute(
            select(Shop).filter(or_(*conditions)))#.options(selectinload(User.relationships)))
            shop = result.scalars().all()

        return shop
    
    @cache(key="get_all_shops")
    async def get_all_shops(self, request:Request):
        async with self.db:
            result = await self.db.execute(
            select(Shop))
            shops = result.scalars().all()
        return  shops
    
    async def create_shop(self, user_data:dict):
        shop = Shop(
            shop_name = user_data['shop_name'],
            address = user_data['address'],
            postal_code = user_data['postal_code'],
            phone = user_data['phone'],
            user_id = user_data['user_id'],
            email = user_data['email']
        )
        self.db.add(shop)
        try:
            await self.db.commit()
            await self.db.refresh(shop)
            return shop
        except SQLAlchemyError as e:
            error_info = str(e.__dict__['orig'])
            await self.db.rollback()
            return JSONResponse(content={"error": "Something went wrong", "detail": error_info},
                                status_code=status.HTTP_409_CONFLICT)