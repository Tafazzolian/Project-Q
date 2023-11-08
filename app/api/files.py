import shutil
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status, Path
from fastapi.responses import JSONResponse, RedirectResponse
from app.services.user_services import UserService
from app.services.otp_services import OtpService
from app.schemas.users_request_models import GetUser, CreateUser, LoginUser, UpdateUser
from app.schemas.users_response_model import UserInfo
from typing import List
from config.authentication import admin_check, login_check

router = APIRouter(prefix="/file", tags=["file"])


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # You can now save the file, process it, etc.
    with open('destination/path/' + file.filename, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}
