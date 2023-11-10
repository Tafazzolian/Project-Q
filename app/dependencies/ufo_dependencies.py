from fastapi import Depends
from app.repositories.ufo_repo import UfoRepository
from app.services.ufo_services import UfoService
from utils.tools import Tools

from .core_dependencies import get_repo_dependency


async def get_ufo_service(repo: UfoRepository = Depends(get_repo_dependency(UfoRepository))):
    return UfoService(repo)
