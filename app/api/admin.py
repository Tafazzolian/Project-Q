from fastapi import APIRouter, Depends, HTTPException, Request, status, Path
from fastapi.responses import HTMLResponse
from app.dependencies.file_dependencies import get_file_service
from app.dependencies.user_dependencies import get_user_service
from app.services.file_services import FileService
from app.services.user_services import UserService

from app.static.template import templates

router = APIRouter(prefix="/admin", tags=["admin"])


# @router.get("/")
# async def get_user(request: Request,request_model: GetUser, user_service: UserService = Depends(get_user_service)):
#     user_data = request_model.model_dump(exclude_unset=True)
#     user = await user_service.get_user(user_data)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

@router.get("/", response_class=HTMLResponse)
async def get_admin_panel(request: Request):
    # Use the corresponding HTML file as the template
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/products", response_class=HTMLResponse)
async def get_admin_panel(request: Request):
    # Use the corresponding HTML file as the template
    return templates.TemplateResponse("products.html", {"request": request})

@router.get("/admin", response_class=HTMLResponse)
async def read_data(request: Request, user_service: UserService = Depends(get_user_service), file_service: FileService = Depends(get_file_service)):
    datam = await user_service.get_all_users(request)
    data = await file_service.get_all_files(request)
    _type = "file"
    return templates.TemplateResponse("admin.html", {"request": request, "data": data,"type":_type})
