from sqlalchemy.orm import Session
from db.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from fastapi import Request, status
from sqlalchemy import or_, text

from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.cache import cache


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user(self,user_data):
        conditions = []
        if "mobile" in user_data:
            conditions.append(User.mobile == user_data["mobile"])
        if "last_name" in user_data:
            conditions.append(User.last_name == user_data["last_name"])
        if "user_id" in user_data:
            conditions.append(User.id == user_data["user_id"])
        if "email" in user_data:
            conditions.append(User.id == user_data["email"])
        
        if not conditions:
            return None
        
        async with self.db:
            result = await self.db.execute(
            select(User).filter(or_(*conditions)))#.options(selectinload(User.relationships)))
            user = result.scalars().first()

        #user = self.db.query(User).filter(or_(*conditions)).first()
        return user
    
    @cache(key="get_all_users")
    async def get_all_users(self, request:Request):
        async with self.db:
            result = await self.db.execute(
            select(User))
            users = result.scalars().all()
        return  users
    

    def create_user(self, first_name, last_name, mobile, password, email=None):
        user = User(
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            email=email,
            hashed_password=User.hash_password(password)
        )
        self.db.add(user)
        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except SQLAlchemyError as e:
            error_info = str(e.__dict__['orig'])
            self.db.rollback()
            return JSONResponse(content={"error": "Something went wrong", "detail": error_info},
                                status_code=status.HTTP_409_CONFLICT)


    def login_user(self, user_data):
        conditions = []
        if "mobile" in user_data:
            conditions.append(User.mobile == user_data["mobile"])
        if "email" in user_data:
            conditions.append(User.id == user_data["email"])

        user = self.db.query(User).filter(or_(*conditions)).first()
        return user
        
        

