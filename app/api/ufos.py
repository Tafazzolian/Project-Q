from fastapi import APIRouter, Depends, HTTPException, Request, status, Path
from fastapi.responses import JSONResponse, RedirectResponse
from app.dependencies.user_dependencies import get_current_user
from app.services.ufo_services import UfoService
from app.services.otp_services import OtpService
from app.schemas.ufos_response_models import GetUfo,CreateUfo
from app.schemas.users_response_models import UserInfo
from typing import List
from config.authentication import admin_check, login_check
from app.dependencies.ufo_dependencies import get_ufo_service

router = APIRouter(prefix="/ufo", tags=["ufo"])

@router.post("/get")
async def get_ufo(request:Request,request_model:GetUfo , ufo_service: UfoService = Depends(get_ufo_service)):
    user_data = request_model.model_dump()
    user_id = get_current_user(request)
    if not user_data['user_id']:
        user_data['user_id'] = int(user_id)
    ufo = await ufo_service.get_ufo(user_data)
    if ufo is None:
        raise HTTPException(status_code=404, detail="User information not found")
    return ufo


@router.post("/create")
async def create_ufo(request:Request,request_model: CreateUfo, ufo_service: UfoService = Depends(get_ufo_service)):
    user_data = request_model.model_dump()
    user_id = await get_current_user(request)
    user_data['user_id']=int(user_id)
    shop = await ufo_service.create_ufo(user_data)
    return shop