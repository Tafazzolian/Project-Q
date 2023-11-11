from db.models.file import File
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request, status
from sqlalchemy import delete, or_, text

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.cache import cache
from utils.tools import Tools


class FileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_file(self,user_data):
        conditions = []
        if "file_id" in user_data:
            conditions.append(File.id        == user_data["file_id"])
        if "link" in user_data:
            conditions.append(File.link      == user_data["link"])
        if "s3_key" in user_data:
            conditions.append(File.s3_key    == user_data["s3_key"])
        if "file_name" in user_data:
            conditions.append(File.file_name == user_data["file_name"])
        
        if not conditions:
            return None
        
        async with self.db:
            result = await self.db.execute(
            select(File).filter(or_(*conditions)))#.options(selectinload(User.relationships)))
            file = result.scalars().first()

        return file
    

    @cache(key="get_all_files")
    async def get_all_files(self, request:Request):
        async with self.db:
            result = await self.db.execute(
            select(File))
            files = result.scalars().all()
        return  files
    

    async def create_file(self, file_name, user_id,link=None, s3_key=None):
        file = File(
            file_name=file_name,
            link=link,
            s3_key=s3_key,
            user_id=user_id
        )
        Tools.red(text="cf1")
        self.db.add(file)
        try:
            await self.db.commit()
            await self.db.refresh(file)
            Tools.green(text="file saved in the db")
            return file
        except SQLAlchemyError as e:
            error_info = str(e.__dict__['orig'])
            Tools.red(text=error_info)
            await self.db.rollback()
            return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error_info)


    async def update_file(self, file_id: int, update_data: dict):
        query = select(File).where(File.id == file_id)
        result = await self.db.execute(query)
        file = result.scalars().first()

        if not file:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

        for key, value in update_data.items():
            setattr(file, key, value)

        try:
            await self.db.commit()
            await self.db.refresh(file)
            return file
        except SQLAlchemyError as e:
            error_info = str(e.__dict__['orig'])
            await self.db.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Something went wrong: {error_info}")
    
    async def delete_file(self, user_data: dict):
        file_id = user_data["file_id"]
        query = delete(File).where(File.id == file_id)
        await self.db.execute(query)
        Tools.red(text=f'{query.file_name} deleted.')