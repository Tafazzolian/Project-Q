from fastapi import APIRouter, Depends, HTTPException, Request, status, Path
from fastapi.responses import JSONResponse, RedirectResponse
from app.services.user_services import UserService
from app.services.otp_services import OtpService
from app.schemas.users_request_models import GetUser, CreateUser, LoginUser, UpdateUser
from app.schemas.users_response_model import UserInfo
from typing import List
from config.authentication import admin_check, login_check

router = APIRouter(prefix="/shop", tags=["shop"])
