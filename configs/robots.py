import os

from fastapi import APIRouter
from starlette.responses import FileResponse

router = APIRouter()


@router.get("/robots.txt", response_class=FileResponse)
async def robots_txt():
    file_path = os.path.join(os.getcwd(), "robots.txt")
    return FileResponse(file_path)
