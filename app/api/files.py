import os
import shutil
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status, Path
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from app.services.user_services import UserService
from app.services.file_services import FileService
from app.schemas.files_request_models import CreateFile
from app.dependencies.file_dependencies import get_file_service
from typing import Dict, List
from config.authentication import admin_check, login_check

router = APIRouter(prefix="/file", tags=["file"])


@router.post("/upload/")
async def upload_file(
    request:Request,
    file: UploadFile = File(...),
    file_name: str = Form(...),
    user_id: int = Form(...),
    link: str = Form(...),
    s3_key: str = Form(...),
    file_service:FileService = Depends(get_file_service)
):
    user_data: Dict[str, str] = {
        "file_name": file.filename,#uniq name
        "user_id": user_id,#get user from token
        "link": link,
        "s3_key": s3_key
    }
    
    await file_service.create_file(request,file,user_data)
    await file.close()
    return {"filename": file_name, "user_data": user_data}


@router.get("/download/{file_id}")#file_id must change to file link
async def download_file(file_id: str, file_service:FileService = Depends(get_file_service)):
    file = await file_service.get_file(user_data={"file_id":int(file_id)})
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")

    filename, file_extension = os.path.splitext(file.filename)
    file_path = os.path.join('files/', file.file_name)
    print(file.file_name)

    # Check if the file exists in the storage
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on server")

    # Return the file using FileResponse which streams the file as a response
    return FileResponse(path=file_path, filename=file.file_name, media_type='application/octet-stream')

@router.get("/get-all-files")
async def get_all_files(request: Request, file_service: FileService = Depends(get_file_service)):
    files = await file_service.get_all_files(request)
    return files
