from fastapi import APIRouter, Depends, HTTPException, Request, status, Path
from fastapi.responses import HTMLResponse
from app.dependencies.file_dependencies import get_file_service
from app.dependencies.user_dependencies import get_user_service
from app.dependencies.ufo_dependencies import get_ufo_service
from app.dependencies.shop_dependencies import get_shop_service
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

# @router.get("/", response_class=HTMLResponse)
# async def get_admin_panel(request: Request):
#     # Use the corresponding HTML file as the template
#     return templates.TemplateResponse("index.html", {"request": request})

@router.get("/products", response_class=HTMLResponse)
async def get_admin_panel(request: Request):
    # Use the corresponding HTML file as the template
    return templates.TemplateResponse("products.html", {"request": request})


@router.get("/{model}", response_class=HTMLResponse)
async def admin_panel(model:str,
                    request: Request,
                    user_service: UserService = Depends(get_user_service),
                    file_service: FileService = Depends(get_file_service),
                    ufo_service: FileService = Depends(get_ufo_service),
                    shop_service: FileService = Depends(get_shop_service)):
    if model == "user":
        data = await user_service.get_all_users(request)
        _type = "user"
    elif model == "file":
        data = await file_service.get_all_files(request)
        _type = "file"
    elif model == "ufo":
        data = await ufo_service.get_all_ufos(request)
        _type = "ufo"
    elif model == "shop":
        data = await shop_service.get_all_shops(request)
        _type = "shop"
    else:
        data = []
        _type = "user"
    return templates.TemplateResponse("admin.html", {"request": request, "data": data,"type":_type})
