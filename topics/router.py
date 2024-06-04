from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from topics.news_file_extractor import news_extractor

router = APIRouter(tags=["Topics"])

templates = Jinja2Templates(directory="templates")


@router.get("/content/{topic}", response_class=HTMLResponse)
async def show_content_html(request: Request, topic: str, limit: int = None):
    print(f"Requested topic: {topic}")
    json_data = await show_content_json(topic, limit)
    data = json_data if isinstance(json_data, dict) and "error" in json_data else {"data": json_data}
    print(data)
    return templates.TemplateResponse("news_list.html", {"request": request, **data})


@router.get("/api/content/{topic}")
async def show_content_json(topic: str, limit: int = None):
    print(f"Requested topic: {topic}")
    return await news_extractor(topic, limit)
