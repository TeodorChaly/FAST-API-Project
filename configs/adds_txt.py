from fastapi.responses import PlainTextResponse
from fastapi import APIRouter

from configs.config_setup import SITE_DOMAIN

router = APIRouter()


@router.get("/ads.txt", response_class=PlainTextResponse, tags=["Bots"])
async def ads_txt():
    robots_file = f""""""
    return PlainTextResponse(content=robots_file)
