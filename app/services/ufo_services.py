import json
import os
import shutil
from fastapi import HTTPException, Request
from app.repositories.ufo_repo import UfoRepository
from utils.tools import Tools


class UfoService:
    def __init__(self, ufo_repository: UfoRepository):
        self.ufo_repository = ufo_repository


    def get_ufo(self, user_data: dict):
        return self.ufo_repository.get_ufo(user_data)
    

    def get_all_ufos(self, request:Request):
        return self.ufo_repository.get_all_ufos(request=request)
    
    def create_ufo(self,user_data:dict):
        return self.ufo_repository.create_ufo(user_data)