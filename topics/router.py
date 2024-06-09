from markupsafe import Markup
from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from topics.news_file_extractor import *

router = APIRouter(tags=["Topics"])

templates = Jinja2Templates(directory="templates")

templates.env.filters['language_name'] = language_to_code


@router.get("/{language}/content/{topic}/{url_part}", response_class=HTMLResponse)
async def show_article_html(request: Request, topic: str, url_part: str, language: str = "en"):
    language_name = get_language_name_by_code(language)
    articles = load_articles_from_json(topic, language_name)
    for article in articles:
        if article.get("url_part") == url_part:
            return templates.TemplateResponse("article_detail.html",
                                              {"request": request, "topic": topic, "article": article})
    return templates.TemplateResponse("error.html", {"request": request, "error": "Article not found."})


@router.get("/{language}/content/{topic}", response_class=HTMLResponse)
async def show_content_html(request: Request, topic: str, language: str = "en", limit: int = None):
    print(f"Requested topic: {topic}")
    json_data = await show_content_json(topic, language, limit)
    if isinstance(json_data, dict) and "error" in json_data:
        return templates.TemplateResponse("error.html", {"request": request, "error": json_data["error"]})

    articles_with_index = []

    for article in json_data:
        if "rewritten_content" in article:
            article["rewritten_content"] = Markup(article["rewritten_content"])
        articles_with_index.append(article)

    return templates.TemplateResponse("news_list.html",
                                      {"request": request, "topic": topic, "articles": articles_with_index})


@router.get("/api/{language}/content/{topic}")
async def show_content_json(topic: str, language: str = "en", limit: int = None):
    language_name = get_language_name_by_code(language)
    print(f"Requested topic: {language_name}")
    return await news_extractor(topic, language_name, limit)
