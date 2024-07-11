from typing import Optional

from fastapi import APIRouter, Request
from markupsafe import Markup
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from content.functions import *
from languages.language_json import languages_to_code
from content.news_file_extractor import *

router = APIRouter()

templates = Jinja2Templates(directory="templates")

templates.env.filters['language_name'] = language_to_code


# @router.get("/{language}/{topic}/{url_part}/detail", response_class=HTMLResponse, tags=["Content"])
# async def show_article_html(request: Request, topic: str, url_part: str, language: str):
#     language_name = get_language_name_by_code(language)
#     articles = load_articles_from_json(topic, language_name)
#     languages = languages_to_code()
#
#     for article in articles:
#         if article.get("url_part") == url_part:
#             return templates.TemplateResponse("article_detail.html",
#                                               {"request": request, "topic": topic, "article": article,
#                                                "language": language, "languages": languages})
#     return templates.TemplateResponse("error.html", {"request": request, "error": "Article not found."})


# @router.get("/change_language/{language}/{topic}", response_class=HTMLResponse, tags=["Content"])
# async def change_language(request: Request, topic: str, url_part: str, language: str, new_language: str):
#     language_name = get_language_name_by_code(language)
#     articles = load_articles_from_json(topic, language_name)
#     languages = languages_to_code()
#
#     for article in articles:
#         if article.get("url_part") == url_part:
#             new_id = article.get("url")
#             language_name = get_language_name_by_code(new_language)
#             json_response = await news_extractor(topic, language_name, None)
#             for i in json_response:
#                 if i.get("url") == new_id:
#                     return templates.TemplateResponse("article_detail.html",
#                                                       {"request": request, "topic": topic, "article": i,
#                                                        "language": new_language, "languages": languages})
#     return templates.TemplateResponse("error.html", {"request": request, "error": "Article not found."})


# @router.get("/{language}/{topic}", response_class=HTMLResponse, tags=["Content"])
# async def show_content_html(request: Request, topic: str, language: str = "en", limit: int = None):
#     print(f"Requested topic: {topic}, {language} language.")
#     json_data = await show_content_json(topic, language, limit)
#
#     if isinstance(json_data, dict) and "error" in json_data:
#         return templates.TemplateResponse("error.html", {"request": request, "error": json_data["error"]})
#
#     articles_with_index = []
#     languages = languages_to_code()
#
#     for article in json_data:
#         if "rewritten_content" in article:
#             article["rewritten_content"] = Markup(article["rewritten_content"])
#         articles_with_index.append(article)
#
#     categories = get_list_of_categories_for_language(articles_with_index)
#
#     return templates.TemplateResponse("news_list.html",
#                                       {"request": request, "topic": topic, "articles": articles_with_index,
#                                        "language": language, "languages": languages, "categories": categories})


# @router.get("/{language}/{topic}/{category}", tags=["Content"])
# async def filter_articles_by_category(request: Request, topic: str, category: str, language: str = "en",
#                                       limit: int = None):
#     language_name = get_language_name_by_code(language)
#     articles = await news_extractor(topic, language_name, limit)
#     languages = languages_to_code()
#
#     filtered_articles = [article for article in articles if article.get("category").lower() == category.lower()]
#
#     if not filtered_articles:
#         return templates.TemplateResponse("error.html",
#                                           {"request": request, "error": f"No articles found in category {category}."})
#
#     return templates.TemplateResponse("categories_list.html",
#                                       {"request": request, "topic": topic, "articles": filtered_articles,
#                                        "language": language, "languages": languages})


@router.get("/api/v1/{language}/{topic}", tags=["API"], response_class=HTMLResponse)
async def show_content_json(topic: str, language: str = "en", limit: int = None):
    try:
        language_name = get_language_name_by_code(language)
        return await news_extractor(topic, language_name, limit)
    except Exception:
        return "Topic or language incorrect"


@router.get("/", tags=["Smart URL"], response_class=HTMLResponse)
async def main_page(request: Request, topic: str = "latvia_google_news", language: str = "en", limit: int = None):
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


@router.get("/{language}/{topic}/{category}", tags=["Content"], response_class=HTMLResponse)
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


@router.get("/{language}/{topic}/{url_part}/detail", tags=["Smart URL"], response_class=HTMLResponse)
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
                                               "trending_news": trending_news})
    return templates.TemplateResponse("error.html", {"request": request, "error": "Article not found."})
