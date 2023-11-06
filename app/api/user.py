from fastapi import APIRouter, Depends, HTTPException, Request, status, Path
from fastapi.responses import JSONResponse, RedirectResponse
from app.services.user_services import UserService
from app.services.otp_service import OtpService
from app.schemas.request_models import GetUser, CreateUser, LoginUser
from app.schemas.response_model import UserInfo
from app.dependencies.dependencies import get_user_service, get_current_user
from typing import List
from config.authentication import login_check

router = APIRouter(prefix="/account", tags=["account"])


@router.post("/get",response_model=UserInfo)
@login_check
async def get_user(request_model: GetUser, user_service: UserService = Depends(get_user_service)):
    user_data = request_model.model_dump()
    user = await user_service.get_user(user_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/get-all",response_model=List[UserInfo])
@login_check
async def get_all_users(request: Request, user_service: UserService = Depends(get_user_service)):
    users = await user_service.get_all_users(request)
    return users

@router.post("/otp/{mobile}")
async def send_otp(mobile:str, request:Request):
    if await OtpService(request).send(mobile=mobile):
        return JSONResponse(
            content={"detail": "code sent"},
            status_code=status.HTTP_201_CREATED
        )
    return JSONResponse(
            content={"detail": "couldn't send code"},
            status_code=status.HTTP_409_CONFLICT
        )


@router.post("/register/{mobile}")
async def create_user(mobile:str, request:Request,request_model: CreateUser, user_service: UserService = Depends(get_user_service)):
    user_data = request_model.model_dump()
    user_data["mobile"] = mobile
    if  await OtpService(request).verify_otp(mobile=user_data["mobile"],code=user_data["code"]):
        user = await user_service.create_user(user_data)
        return user
    return JSONResponse(
            content={"detail": "wrong otp"},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    


@router.post("/login")
async def login_for_access_token(request:Request,
    request_model: LoginUser, 
    user_service: UserService = Depends(get_user_service)
):
    if request.state.status == "Good_token":
        return JSONResponse(
            content={"detail": "You are already logged in."},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    user_data = request_model.model_dump()
    user = await user_service.login_user(user_data, request)
    return user


@router.post("/logout")
async def log_out(request:Request, user_service: UserService = Depends(get_user_service)):

    if request.state.status == "Good_token":
        await user_service.log_out(request=request)
        message = {"message": "Logged out successfully."}
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    else:
        message = {"message": "You are not logged in"}
        response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return message, response