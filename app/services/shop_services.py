import json
import os
import shutil
from fastapi import HTTPException, Request
from app.repositories.shop_repo import ShopRepository
from utils.tools import Tools


class ShopService:
    def __init__(self, shop_repository: ShopRepository):
        self.shop_repository = shop_repository


    def get_shop(self, user_data: dict):
        return self.shop_repository.get_shop(user_data)
    

    def get_all_shops(self, request:Request):
        return self.shop_repository.get_all_shops(request=request)
    
    def create_shop(self,user_data:dict):
        return self.shop_repository.create_shop(user_data)