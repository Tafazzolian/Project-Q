from fastapi import Depends
from app.repositories.shop_repo import ShopRepository
from app.services.shop_services import ShopService
from utils.tools import Tools

from .core_dependencies import get_repo_dependency


async def get_shop_service(repo: ShopRepository = Depends(get_repo_dependency(ShopRepository))):
    return ShopService(repo)
