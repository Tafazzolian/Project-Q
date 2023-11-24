from fastapi import APIRouter, Depends, HTTPException, Request, status, Path
from fastapi.responses import JSONResponse, RedirectResponse
from app.dependencies.user_dependencies import get_current_user
from app.services.shop_services import ShopService
from app.services.otp_services import OtpService
from app.schemas.shops_request_models import GetShopRequestModel, CreateShopRequestModel
from app.schemas.users_response_models import UserInfo
from typing import List
from config.authentication import admin_check, login_check
from app.dependencies.shop_dependencies import get_shop_service

router = APIRouter(prefix="/shop", tags=["shop"])

@router.post("/get")
async def get_shop(request_model: GetShopRequestModel, shop_service: ShopService = Depends(get_shop_service)):
    user_data = request_model.model_dump(exclude_unset=True)
    shop = await shop_service.get_shop(user_data)
    if shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return shop

@router.post("/create")
async def create_shop(request:Request,request_model: CreateShopRequestModel, shop_service: ShopService = Depends(get_shop_service)):
    user_data = request_model.model_dump()
    user_id = await get_current_user(request)
    user_data['user_id']=int(user_id)
    shop = await shop_service.create_shop(user_data)
    return shop