from fastapi import APIRouter, Depends, HTTPException
from app.services.user_services import UserService
from app.schemas.request_models import GetUser, CreateUser, LoginUser
from app.dependencies.dependencies import get_user_service


router = APIRouter(prefix="/account", tags=["account"])


@router.get("/get")
async def get_user(request_model: GetUser, user_service: UserService = Depends(get_user_service)):
    user = user_service.get_user(**request_model.model_dump())
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user.id, "username": user.first_name}


@router.post("/register")
async def create_user(request_model: CreateUser, user_service: UserService = Depends(get_user_service)):
    user_data = request_model.model_dump()
    user = user_service.create_user(**user_data)
    return user



# @router.post("/login")
# async def create_user(request_model: LoginUser, user_service: UserService = Depends(UserService)):
#     user = user_service.login_user(**request_model.model_dump())
#     return user
