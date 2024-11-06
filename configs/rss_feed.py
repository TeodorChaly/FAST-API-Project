import json
import os
from datetime import datetime
from fastapi import APIRouter
from starlette.responses import PlainTextResponse

from configs.config_setup import SITE_DOMAIN, main_site_topic, main_language
from content.news_file_extractor import language_to_code, get_language_name_by_code
from languages.language_json import language_json_read
from main_operations.scraper.json_save import get_main_info

router = APIRouter()


# Объединение двух маршрутов
@router.get("/rss", response_class=PlainTextResponse, tags=["RSS"])
@router.get("/feed", response_class=PlainTextResponse, tags=["RSS"])
async def rss_feed(language: str = main_language):
    return await rss_feed_function(language)


async def rss_feed_function(language: str):
    languages = await language_json_read()

    encrypted_languages = [language_to_code(full_language) for full_language in languages]
    if language not in encrypted_languages:
        return PlainTextResponse(content="RSS feed for this language not found", status_code=404)

    rss_content = await generate_rss_feed(language)
    return PlainTextResponse(content=rss_content, media_type="application/rss+xml; charset=utf-8")


async def generate_rss_feed(language: str) -> str:
    rss_items = get_content_from_json_files(language)
    rss_items = rss_items[:20]

    info_translate = get_main_info(language, main_site_topic)
    if not info_translate:
        print(f"Info for {language} not found")
        return PlainTextResponse(content="RSS feed info not found", status_code=404)

    last_article_date = max(
        (datetime.strptime(item['lastmod'], '%Y-%m-%dT%H:%M:%SZ') for item in rss_items),
        default=datetime.utcnow()
    ).strftime('%a, %d %b %Y %H:%M:%S +0000')

    rss_feed = """<?xml version="1.0" encoding="UTF-8"?>\n"""
    rss_feed += """<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n"""
    rss_feed += """   <channel>\n"""
    rss_feed += f"      <title>{info_translate['main_page']['seo_title']}</title>\n"
    rss_feed += f"      <link>{SITE_DOMAIN}</link>\n"
    rss_feed += f"      <description>{info_translate['main_page']['seo_description']}</description>\n"
    rss_feed += f"      <lastBuildDate>{last_article_date}</lastBuildDate>\n"
    rss_feed += f"      <language>{language}</language>\n"
    rss_feed += f"      <atom:link href='{SITE_DOMAIN}/rss_{language}.xml' rel='self' type='application/rss+xml' />\n"

    for item in rss_items:
        rss_feed += "      <item>\n"
        title = item.get('seo_title', None)
        seo_description = item.get('seo_description', None)

        rss_feed += f"         <title>{title}</title>\n"
        rss_feed += f"         <link>{item['loc']}</link>\n"
        rss_feed += f"         <description>{seo_description}</description>\n"

        category = item.get('category', 'Uncategorized')
        rss_feed += f"         <category>{category}</category>\n"

        author = item.get('author', 'Unknown Author')
        rss_feed += f"         <author>{author}</author>\n"

        # Используем вспомогательную функцию для обработки даты
        pub_date = get_pub_date(item.get('lastmod'))
        rss_feed += f"         <pubDate>{pub_date}</pubDate>\n"

        rss_feed += f"         <guid>{item['loc']}</guid>\n"
        rss_feed += "      </item>\n"

    rss_feed += "   </channel>\n"
    rss_feed += "</rss>"

    return rss_feed


def get_pub_date(lastmod: str) -> str:
    """Обрабатывает формат даты и возвращает строку для <pubDate>"""
    try:
        if lastmod and lastmod != "-":
            pub_date = datetime.strptime(lastmod, '%Y-%m-%dT%H:%M:%SZ').strftime('%a, %d %b %Y %H:%M:%S +0000')
        else:
            pub_date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')
    except ValueError:
        print(f"Invalid date format in lastmod: {lastmod}")
        pub_date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')

    return pub_date


def get_content_from_json_files(language: str):
    full_language = get_language_name_by_code(language)
    directory = f'news_json/{main_site_topic}/'

    filepath = os.path.join(directory, f"{main_site_topic}_{full_language}.json")
    urls_list = []

    # Обработка ошибок при открытии файла
    if not os.path.exists(filepath):
        print(f"File {filepath} not found.")
        return urls_list

    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data_list = json.load(f)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {filepath}")
            return urls_list

        # Получаем последние 20 статей
        data_list = data_list[:20]

        for data in data_list:
            url_part = data.get('url_part')
            category = data.get('category')
            seo_title = data.get('seo_title')
            seo_description = data.get('seo_description')
            author = data.get('author')
            image = data.get('image')
            date_published = data.get('date_published')

            # Формирование даты публикации
            try:
                date_obj = datetime.strptime(date_published, "%d %m %Y %H:%M")
                lastmod = date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
            except Exception as e:
                lastmod = date_published

            language = data.get('language', 'en')
            language_code = language_to_code(language)

            url = f"{SITE_DOMAIN}/{language_code}/{category}/{url_part}"
            urls_list.append({
                "loc": url,
                "seo_title": seo_title,
                "seo_description": seo_description,
                "lastmod": lastmod,
                "image": image,
                "category": category,
                "author": author
            })

    return urls_list
