from typing import Optional

from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from content.functions import *
from content.news_file_extractor import *
from configs.config_setup import main_site_topic
from languages.language_json import languages_to_code

router = APIRouter()

templates = Jinja2Templates(directory="templates")

templates.env.filters['language_name'] = language_to_code


async def show_content_json(topic: str, language: str = "en", limit: int = None):
    try:
        language_name = get_language_name_by_code(language)
        return await news_extractor(topic, language_name, limit)
    except Exception:
        return "Topic or language incorrect"


@router.get("/", tags=["User content"], response_class=HTMLResponse)
async def main_page_redirect():
    redirect = main_site_topic
    return RedirectResponse(url=f"/{redirect}")


@router.get("/{topic}", tags=["User content"], response_class=HTMLResponse)
async def main_page(request: Request, topic: str, language: str = "en", limit: int = None):
    print(f"Requested topic: {topic}, {language} language.")
    languages = languages_to_code()

    json_data = await show_content_json(topic, language, limit)

    if isinstance(json_data, dict) and "error" in json_data:
        return templates.TemplateResponse("error.html", {"request": request, "error": json_data["error"]})

    newest_news_len = 5
    today_news_len = 10

    today_news_all = await show_content_json(topic, language, today_news_len + newest_news_len)
    newest_news = today_news_all[:newest_news_len]
    today_news = today_news_all[newest_news_len:]

    popular_categories, remaining_categories, all_categories = await get_categories(topic, json_data)

    # print("Top 5 categories:", popular_categories)
    # print("Remaining categories:", remaining_categories)

    content = content_all(all_categories, json_data)

    return templates.TemplateResponse("main_page_news.html",
                                      {"request": request, "topic": topic, "language": language, "languages": languages,
                                       "top_categories": popular_categories, "other_categories": remaining_categories,
                                       "newest_news": newest_news, "all_content": content, "today_news": today_news
                                       })


@router.get("/{language}/{topic}/{category}", tags=["User content"], response_class=HTMLResponse)
async def category_list(request: Request, topic: str, category: str, language: str = "en",
                        limit: Optional[int] = None, page: int = 1):
    language_name = get_language_name_by_code(language)
    articles = await news_extractor(topic, language_name, limit)
    languages = languages_to_code()

    json_data = await show_content_json(topic, language, limit)
    popular_categories, remaining_categories, all_categories = await get_categories(topic, json_data)

    trending_categories = get_trending_categories(all_categories)

    trending_news = await show_content_json(topic, language, 4)

    filtered_articles, total_pages = get_all_articles(articles, category, page)

    if not filtered_articles and page == 1 or page <= 0:
        return templates.TemplateResponse("error.html",
                                          {"request": request, "error": f"No articles found in category {category}."})

    return templates.TemplateResponse("category_list_template.html",
                                      {"request": request, "topic": topic, "category": category, "language": language,
                                       "articles": filtered_articles, "languages": languages,
                                       "top_categories": popular_categories, "other_categories": remaining_categories,
                                       "trending_categories": trending_categories, "trending_news": trending_news,
                                       "page": page, "total_pages": total_pages})


@router.get("/{language}/{topic}/{url_part}/detail", tags=["User content"], response_class=HTMLResponse)
async def article_detail(request: Request, topic: str, url_part: str, language: str):
    language_name = get_language_name_by_code(language)
    articles = load_articles_from_json(topic, language_name)
    languages = languages_to_code()

    json_data = await show_content_json(topic, language, None)  # Modify!!!
    popular_categories, remaining_categories, all_categories = await get_categories(topic, json_data)

    trending_categories = get_trending_categories(all_categories)
    trending_news = await show_content_json(topic, language, 4)

    for article in articles:
        if article.get("url_part") == url_part:
            return templates.TemplateResponse("article-details.html",
                                              {"request": request, "topic": topic, "article": article,
                                               "language": language, "languages": languages,
                                               "top_categories": popular_categories,
                                               "other_categories": remaining_categories,
                                               "trending_categories": trending_categories,
                                               "trending_news": trending_news, "tags": article["tags"].split(",")})
    return templates.TemplateResponse("error.html", {"request": request, "error": "Article not found."})
