from fastapi import Depends, HTTPException
from app.repositories.user_repo import UserRepository
from app.services.user_services import UserService
from typing import Any, Optional
from starlette.requests import Request
from config.authentication import AccessToken
from utils.tools import Tools

from .core_dependencies import get_repo_dependency



async def get_user_service(repo: UserRepository = Depends(get_repo_dependency(UserRepository))):
    return UserService(repo)

# async def get_user_service(repo: UserRepository = Depends(inject_session_to_repo(repository= UserRepository))) -> UserService:
#     return UserService(repo)


async def get_current_user(request: Request, token: Optional[str] = None):
    if not token:
        token = request.state.token
    user_id = await AccessToken().check_token(token, request)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    return user_id