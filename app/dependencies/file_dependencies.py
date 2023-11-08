from fastapi import Depends
from app.repositories.file_repo import FileRepository
from app.services.file_services import FileService
from utils.tools import Tools

from .core_dependencies import get_repo_dependency


async def get_file_service(repo: FileRepository = Depends(get_repo_dependency(FileRepository))):
    return FileService(repo)

