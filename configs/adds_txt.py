from fastapi.responses import PlainTextResponse
from fastapi import APIRouter

router = APIRouter()


@router.get("/ads.txt", response_class=PlainTextResponse, tags=["Bots"])
async def ads_txt():
    robots_file = f""""""
    return PlainTextResponse(content=robots_file)