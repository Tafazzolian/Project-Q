from sqlalchemy.orm import Session
from db.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request, status
from sqlalchemy import delete, or_, text

from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.cache import cache


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user(self,user_data):
        conditions = []
        if "user_id" in user_data:
            conditions.append(User.id        == user_data["user_id"])
        if "mobile" in user_data:
            conditions.append(User.mobile    == user_data["mobile"])
        if "email" in user_data:
            conditions.append(User.email     == user_data["email"])
        if "last_name" in user_data:
            conditions.append(User.last_name == user_data["last_name"])
        
        if not conditions:
            return None
        
        async with self.db:
            result = await self.db.execute(
            select(User).filter(or_(*conditions)))#.options(selectinload(User.relationships)))
            user = result.scalars().first()

        return user
    
    @cache(key="get_all_users")
    async def get_all_users(self, request:Request):
        async with self.db:
            result = await self.db.execute(
            select(User))
            users = result.scalars().all()
        return  users
    

    async def create_user(self, first_name, last_name, mobile, password, email=None):
        user = User(
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            email=email,
            hashed_password=User.hash_password(password)
        )
        self.db.add(user)
        try:
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except SQLAlchemyError as e:
            error_info = str(e.__dict__['orig'])
            await self.db.rollback()
            return JSONResponse(content={"error": "Something went wrong", "detail": error_info},
                                status_code=status.HTTP_409_CONFLICT)


    async def update_user(self, user_id: int, update_data: dict):
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        user = result.scalars().first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        for key, value in update_data.items():
            setattr(user, key, value)

        try:
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except SQLAlchemyError as e:
            error_info = str(e.__dict__['orig'])
            await self.db.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Something went wrong: {error_info}")
    

    async def delete_user(self, user_data: dict):
        user_id = user_data["user_id"]
        query = delete(User).where(User.id == user_id)
        await self.db.execute(query)
        
        

