from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from app.services.user_services import UserService
from app.schemas.request_models import GetUser, CreateUser, LoginUser
from app.schemas.response_model import UserInfo
from app.dependencies.dependencies import get_user_service, get_current_user, already_logged_in_check
from typing import List, Optional
from config.cache import cache

from db.models.user import User

router = APIRouter(prefix="/account", tags=["account"])

@router.post("/get",response_model=UserInfo)
async def get_user(request_model: GetUser, user_service: UserService = Depends(get_user_service)):
    user_data = request_model.model_dump()
    user = user_service.get_user(user_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/get-all", response_model=List[UserInfo])
async def get_all_users(user_service: UserService = Depends(get_user_service), current_user = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized_Access")
    
    if "get_all_users" in cache:
        print('cache worked')
        return cache["get_all_users"]
    else:
        users = user_service.get_all_users()
        cache.set("get_all_users",users,expire=5)
        return users


@router.post("/register")
async def create_user(request_model: CreateUser, user_service: UserService = Depends(get_user_service)):
    user_data = request_model.model_dump()
    user = user_service.create_user(user_data)
    return user


@router.post("/login")
async def login_for_access_token(
    request_model: LoginUser, 
    user_service: UserService = Depends(get_user_service),
    user_login_status: Optional[User] = Depends(already_logged_in_check)
):
    if user_login_status:
        return JSONResponse(
            content={"detail": "You are already logged in."},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    user_data = request_model.model_dump()
    user = user_service.login_user(user_data)
    return user


@router.post("/logout")
async def log_out(request:Request,
                  user_service: UserService = Depends(get_user_service),
                  user_login_status: Optional[User] = Depends(already_logged_in_check)):
    if user_login_status:
        user_service.log_out(request=request)
        message = {"message": "Logged out successfully."}
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    else:
        message = {"message": "You are not logged in"}
        response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return message, response