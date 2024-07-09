from markupsafe import Markup
from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from languages.language_json import languages_to_code
from content.news_file_extractor import *
from main_operations.scraper.json_save import categories_extractor

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


@router.get("/smart_url", tags=["Smart URL"])
async def smart_url(request: Request, topic: str, language: str = "en", limit: int = None):
    print(f"Requested topic: {topic}, {language} language.")
    json_data = await show_content_json(topic, language, limit)

    if isinstance(json_data, dict) and "error" in json_data:
        return templates.TemplateResponse("error.html", {"request": request, "error": json_data["error"]})

    articles_with_index = []
    languages = languages_to_code()
    # Fix to many data!!!
    for article in json_data:
        if "rewritten_content" in article:
            article["rewritten_content"] = Markup(article["rewritten_content"])
        articles_with_index.append(article)

    max_list_len = 5

    categories = {}
    for article in articles_with_index:
        category = article.get("category", "Uncategorized")
        if category not in categories:
            categories[category] = []
        if len(categories[category]) < max_list_len:
            categories[category].append(article)

    categories = {category: articles for category, articles in categories.items() if len(articles) >= max_list_len}
    # limit articles to max_list_len
    articles_with_index = articles_with_index[:max_list_len]

    return templates.TemplateResponse("main_page_news.html",
                                      {"request": request, "topic": topic, "articles": articles_with_index,
                                       "language": language, "languages": languages, "categories": categories})


@router.get("/language", tags=["Smart URL"])
async def smart_by_category(request: Request, topic: str, category: str, language: str = "en",
                            limit: int = None):
    language_name = get_language_name_by_code(language)
    articles = await news_extractor(topic, language_name, limit)
    languages = languages_to_code()

    filtered_articles = [article for article in articles if article.get("category").lower() == category.lower()]

    if not filtered_articles:
        return templates.TemplateResponse("error.html",
                                          {"request": request, "error": f"No articles found in category {category}."})

    return templates.TemplateResponse("category_list_template.html",
                                      {"request": request, "topic": topic, "articles": filtered_articles,
                                       "language": language, "languages": languages})


@router.get("/detail", tags=["Smart URL"])
async def smart_article_html(request: Request, topic: str, url_part: str, language: str):
    language_name = get_language_name_by_code(language)
    articles = load_articles_from_json(topic, language_name)
    languages = languages_to_code()

    for article in articles:
        if article.get("url_part") == url_part:
            return templates.TemplateResponse("article-details.html",
                                              {"request": request, "topic": topic, "article": article,
                                               "language": language, "languages": languages})
    return templates.TemplateResponse("error.html", {"request": request, "error": "Article not found."})


@router.get("/test", tags=["Smart URL"])
async def test(request: Request, topic: str, language: str = "en", limit: int = None):
    print(f"Requested topic: {topic}, {language} language.")
    json_data = await show_content_json(topic, language, limit)

    newest_news_len = 5
    today_news_len = 10

    today_news = await show_content_json(topic, language, today_news_len + newest_news_len)
    newest_news = today_news[:newest_news_len]
    today_news = today_news[newest_news_len:]

    get_all_categories = await categories_extractor(topic)
    items = [item.strip() for item in get_all_categories.splitlines()]
    categories_list = [item.strip('",[]') for item in items if item.strip('",[]')]
    article_res = get_list_of_categories_for_language_2(json_data, categories_list)

    popular_categories, remaining_categories = split_categories_by_frequency(article_res)
    print("Top 5 categories:", popular_categories)
    print("Remaining categories:", remaining_categories)

    if isinstance(json_data, dict) and "error" in json_data:
        return templates.TemplateResponse("error.html", {"request": request, "error": json_data["error"]})

    articles_with_index = []
    languages = languages_to_code()
    # Fix to many data!!!
    for article in json_data:
        if "rewritten_content" in article:
            article["rewritten_content"] = Markup(article["rewritten_content"])
        articles_with_index.append(article)

    max_list_len = 5

    categories = {}
    for article in articles_with_index:
        category = article.get("category", "Uncategorized")
        if category not in categories:
            categories[category] = []
        if len(categories[category]) < max_list_len:
            categories[category].append(article)

    categories = {category: articles for category, articles in categories.items() if len(articles) >= max_list_len}

    return templates.TemplateResponse("main_page_news.html",
                                      {"request": request, "topic": topic, "language": language, "languages": languages,
                                       "top_categories": popular_categories, "other_categories": remaining_categories,
                                       "newest_news": newest_news, "categories": categories, "today_news": today_news
                                       })
