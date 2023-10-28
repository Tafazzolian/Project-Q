from fastapi import APIRouter, Depends, HTTPException
from app.services.user_services import UserService
from app.schemas.request_models import GetUser, CreateUser, LoginUser
from app.schemas.response_model import UserInfo
from app.dependencies.dependencies import get_user_service
from typing import List


router = APIRouter(prefix="/account", tags=["account"])

@router.get("/get",response_model=UserInfo)
async def get_user(request_model: GetUser, user_service: UserService = Depends(get_user_service)):
    user_data = request_model.model_dump()
    user = user_service.get_user(user_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/get-all", response_model=List[UserInfo])
async def get_user(user_service: UserService = Depends(get_user_service)):
    user = user_service.get_all_users()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/register")
async def create_user(request_model: CreateUser, user_service: UserService = Depends(get_user_service)):
    user_data = request_model.model_dump()
    user = user_service.create_user(**user_data)
    return user



# @router.post("/token")
# async def login_for_access_token(form_data: Login, user_service: UserService = Depends(get_user_service)):

#     user = db.query(User).filter(User.username == form_data.username).first()
#     if not user or not user.verify_password(form_data.password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# @router.post("/login")
# async def create_user(request_model: LoginUser, user_service: UserService = Depends(UserService)):
#     user = user_service.login_user(**request_model.model_dump())
#     return user
