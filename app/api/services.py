from fastapi import APIRouter, Depends, HTTPException, Request, status, Path
from fastapi.responses import JSONResponse, RedirectResponse
from app.services.otp_services import OtpService
from app.schemas.services_request_models import Otp
from app.dependencies.user_dependencies import get_user_service, get_current_user
from typing import List
from config.authentication import admin_check, login_check

router = APIRouter(prefix="/service", tags=["service"])

@router.post("/otp")
async def send_otp(request_model:Otp, request:Request):
    user_data = request_model.model_dump()
    mobile = user_data["mobile"]
    if await OtpService(request).send(mobile=mobile):
        return JSONResponse(
            content={"detail": "code sent"},
            status_code=status.HTTP_201_CREATED
        )
    return JSONResponse(
            content={"detail": "couldn't send code"},
            status_code=status.HTTP_409_CONFLICT
        )

@router.post("/shaba-creator")
async def shaba_creator(request_model:Otp, request:Request):
    user_data = request_model.model_dump()
    mobile = user_data["mobile"]
    if await OtpService(request).send(mobile=mobile):
        return JSONResponse(
            content={"detail": "code sent"},
            status_code=status.HTTP_201_CREATED
        )
    return JSONResponse(
            content={"detail": "couldn't send code"},
            status_code=status.HTTP_409_CONFLICT
        )

