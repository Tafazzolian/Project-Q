from fastapi import APIRouter, Depends, HTTPException, Request, status, Path
from fastapi.responses import JSONResponse, RedirectResponse
from app.services.user_services import UserService
from app.services.otp_services import OtpService
from app.schemas.users_request_models import GetUser, CreateUser, LoginUser, UpdateUser
from app.schemas.users_response_models import UserInfo
from app.dependencies.user_dependencies import get_user_service, get_current_user
from typing import List
from config.authentication import admin_check, login_check

router = APIRouter(prefix="/account", tags=["account"])


@router.post("/get",response_model=UserInfo)
@login_check
async def get_user(request: Request,request_model: GetUser, user_service: UserService = Depends(get_user_service)):
    user_data = request_model.model_dump(exclude_unset=True)
    user = await user_service.get_user(user_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/get-all",response_model=List[UserInfo])
# @admin_check
# @login_check
async def get_all_users(request: Request, user_service: UserService = Depends(get_user_service)):
    users = await user_service.get_all_users(request)
    return users


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


@router.put("/update-user")
async def update_user(request:Request,request_model: UpdateUser, user_service: UserService = Depends(get_user_service), current_user = Depends(get_current_user)):
    user_data = request_model.model_dump(exclude_unset=True)
    user_id =  current_user
    if user_data and user_id:
        user = await user_service.update_user(int(user_id), user_data)
        return user
    return JSONResponse(
            content={"detail": "you didn't change anything"},
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
    user_data = request_model.model_dump(exclude_unset=True)
    user = await user_service.login_user(user_data, request)
    return user


@router.post("/logout")
@login_check
async def log_out(request:Request, user_service: UserService = Depends(get_user_service)):

    await user_service.log_out(request=request)
    message = {"message": "Logged out successfully."}
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

    return message, response