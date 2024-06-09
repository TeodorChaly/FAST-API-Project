import json

from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from topics.news_file_extractor import *

router = APIRouter(tags=["Topics"])

templates = Jinja2Templates(directory="templates")


@router.get("/content/{topic}/{article_id}", response_class=HTMLResponse)
async def show_article_html(request: Request, topic: str, article_id: int, language: str = "english"):
    articles = load_articles_from_json(topic, language)
    for article in articles:
        if article.get("id") == article_id:
            return templates.TemplateResponse("article_detail.html",
                                              {"request": request, "topic": topic, "article": article})
    return templates.TemplateResponse("error.html", {"request": request, "error": "Article not found."})


@router.get("/content/{topic}", response_class=HTMLResponse)
async def show_content_html(request: Request, topic: str, language: str = "english", limit: int = None):
    print(f"Requested topic: {topic}")
    json_data = await show_content_json(topic, language, limit)
    if isinstance(json_data, dict) and "error" in json_data:
        return templates.TemplateResponse("error.html", {"request": request, "error": json_data["error"]})

    articles_with_index = [article for article in json_data if "id" in article]

    return templates.TemplateResponse("news_list.html",
                                      {"request": request, "topic": topic, "articles": articles_with_index})


@router.get("/api/content/{topic}")
async def show_content_json(topic: str, language: str = "english", limit: int = None):
    print(f"Requested topic: {topic}")
    return await news_extractor(topic, language, limit)
