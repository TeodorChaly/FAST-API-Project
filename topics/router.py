from markupsafe import Markup
from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from languages.language_json import languages_to_code
from topics.news_file_extractor import *

router = APIRouter()

templates = Jinja2Templates(directory="templates")

templates.env.filters['language_name'] = language_to_code


@router.get("/{language}/{topic}/{url_part}/detail", response_class=HTMLResponse, tags=["Content"])
async def show_article_html(request: Request, topic: str, url_part: str, language: str):
    language_name = get_language_name_by_code(language)
    articles = load_articles_from_json(topic, language_name)
    languages = languages_to_code()

    for article in articles:
        if article.get("url_part") == url_part:
            return templates.TemplateResponse("article_detail.html",
                                              {"request": request, "topic": topic, "article": article,
                                               "language": language, "languages": languages})
    return templates.TemplateResponse("error.html", {"request": request, "error": "Article not found."})


@router.get("/change_language/{language}/{topic}", response_class=HTMLResponse, tags=["Content"])
async def change_language(request: Request, topic: str, url_part: str, language: str, new_language: str):
    language_name = get_language_name_by_code(language)
    articles = load_articles_from_json(topic, language_name)
    languages = languages_to_code()

    for article in articles:
        if article.get("url_part") == url_part:
            new_id = article.get("url")
            language_name = get_language_name_by_code(new_language)
            json_response = await news_extractor(topic, language_name, None)
            for i in json_response:
                if i.get("url") == new_id:
                    return templates.TemplateResponse("article_detail.html",
                                                      {"request": request, "topic": topic, "article": i,
                                                       "language": new_language, "languages": languages})
    return templates.TemplateResponse("error.html", {"request": request, "error": "Article not found."})


@router.get("/{language}/{topic}", response_class=HTMLResponse, tags=["Content"])
async def show_content_html(request: Request, topic: str, language: str = "en", limit: int = None):
    print(f"Requested topic: {topic}, {language} language.")
    json_data = await show_content_json(topic, language, limit)

    if isinstance(json_data, dict) and "error" in json_data:
        return templates.TemplateResponse("error.html", {"request": request, "error": json_data["error"]})

    articles_with_index = []
    languages = languages_to_code()

    for article in json_data:
        if "rewritten_content" in article:
            article["rewritten_content"] = Markup(article["rewritten_content"])
        articles_with_index.append(article)

    categories = get_list_of_categories_for_language(articles_with_index)

    return templates.TemplateResponse("news_list.html",
                                      {"request": request, "topic": topic, "articles": articles_with_index,
                                       "language": language, "languages": languages, "categories": categories})


@router.get("/{language}/{topic}/{category}", tags=["Content"])
async def filter_articles_by_category(request: Request, topic: str, category: str, language: str = "en",
                                      limit: int = None):
    language_name = get_language_name_by_code(language)
    articles = await news_extractor(topic, language_name, limit)
    languages = languages_to_code()

    filtered_articles = [article for article in articles if article.get("category").lower() == category.lower()]

    if not filtered_articles:
        return templates.TemplateResponse("error.html",
                                          {"request": request, "error": f"No articles found in category {category}."})

    return templates.TemplateResponse("categories_list.html",
                                      {"request": request, "topic": topic, "articles": filtered_articles,
                                       "language": language, "languages": languages})


@router.get("/api/v1/{language}/{topic}", tags=["API"])
async def show_content_json(topic: str, language: str = "en", limit: int = None):
    try:
        language_name = get_language_name_by_code(language)
        return await news_extractor(topic, language_name, limit)
    except Exception:
        return "Topic or language incorrect"
