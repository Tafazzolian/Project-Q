import json
import os
import shutil
from fastapi import HTTPException, Request
from app.repositories.file_repo import FileRepository

from utils.tools import Tools


class FileService:
    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository


    def get_file(self, user_data: dict):
        return self.file_repository.get_file(user_data)
    

    def get_all_files(self, request:Request):
        return self.file_repository.get_all_files(request=request)
    

    async def create_file(self, request,file,user_data: dict):
        if not os.path.exists('files/'):
            os.makedirs('files/', exist_ok=True)
            
        file_path = os.path.join('files/', file.filename)
        # Write the file to the filesystem
        try:
            with open(file_path, 'wb') as buffer:
                shutil.copyfileobj(file.file, buffer)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        job_data = {
        "file_path": file_path,
        "file_name": user_data["file_name"],
                    }
        redis_conn = request.app.state.redis
        await redis_conn.lpush('file_queue', json.dumps(job_data))
        Tools.yellow(text="file added to redis que")

        return self.file_repository.create_file(
            file_name=user_data["file_name"],
            user_id = user_data["user_id"],
            link=user_data["link"],
            s3_key=user_data["s3_key"]
            )
    
    
    def update_file(self, file_id:int, user_data:dict):
        return self.file_repository.update_file(file_id, user_data)
    

    def delete_file(self,user_data:dict):
        return self.file_repository.delete_file(user_data)