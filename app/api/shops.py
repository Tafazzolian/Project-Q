from fastapi import APIRouter, Depends, HTTPException, Request, status, Path
from fastapi.responses import JSONResponse, RedirectResponse
from app.services.user_services import UserService
from app.services.otp_services import OtpService
from app.schemas.users_request_models import GetUser, CreateUser, LoginUser, UpdateUser
from app.schemas.users_response_model import UserInfo
from app.dependencies.dependencies import get_user_service, get_current_user
from typing import List
from config.authentication import admin_check, login_check

router = APIRouter(prefix="/shop", tags=["shop"])


@router.post("/get",response_model=UserInfo)
@login_check
async def get_user(request: Request,request_model: GetUser, user_service: UserService = Depends(get_user_service)):
    user_data = request_model.model_dump(exclude_unset=True)
    user = await user_service.get_user(user_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user