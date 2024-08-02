import json
import os
import logging
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from configs.config_setup import main_site_topic
from content.news_file_extractor import language_to_code
from languages.language_json import language_json_read, languages_to_code
from main_operations.router import router as scraping_router
from content.router import router as topics_router
from languages.router import router as languages_router
from main_operations.crawlers.RSS_crawler.router import router as crawler_router
from main_operations.scraper.json_save import categories_extractor

logging.basicConfig(
    filename='access.log',
    level=logging.INFO,
    format='%(asctime)s - IP: %(clientip)s, User-Agent: %(useragent)s, Method: %(method)s, Path: %(path)s'
)

app = FastAPI(
    title="News generator API",
    version="0.1"
)

app.mount("/assets", StaticFiles(directory="templates/assets"), name="assets")


@app.on_event("startup")
async def startup_event():
    file_path = "languages/languages.json"
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(["english"], file)

    if not os.path.exists("scraped_urls.json"):
        with open("scraped_urls.json", 'w', encoding='utf-8') as file:
            json.dump([], file)


# Middleware production
@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    client_ip = request.client.host
    user_agent = request.headers.get('user-agent', 'Unknown')
    method = request.method
    path = request.url.path

    logging.info(
        '',
        extra={
            'clientip': client_ip,
            'useragent': user_agent,
            'method': method,
            'path': path
        }
    )

    response = await call_next(request)
    return response


def get_urls_from_json_files() -> list[dict]:
    directory = f'news_json/{main_site_topic}'
    urls = []
    categories = json.loads(categories_extractor(main_site_topic))
    languages = language_json_read()

    for language in languages:
        language = language_to_code(language)
        url = f"http://127.0.0.1:8000/{main_site_topic}?language={language}"
        urls.append({
            "loc": url,
            "lastmod": datetime.now().strftime("%d %m %Y"),
            "changefreq": "daily",
            "priority": "1.0"
        })

    for category in categories:
        for language in languages:
            language = language_to_code(language)
            url = f"http://127.0.0.1:8000/{language}/{main_site_topic}/{category}"
            urls.append({
                "loc": url,
                "lastmod": datetime.now().strftime("%d %m %Y"),
                "changefreq": "daily",
                "priority": "1.0"
            })


    for filename in os.listdir(directory):
        if filename.endswith(".json") and filename.startswith(f"{main_site_topic}_") and not filename.startswith(
                f"{main_site_topic}__category"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data_list = json.load(f)
                for data in data_list:
                    url_part = data.get('url_part')
                    date_published = data.get('date_published')
                    language = data.get('language', 'en')
                    language = language_to_code(language)

                    url = f"http://127.0.0.1:8000/{language}/{main_site_topic}/{url_part}/detail"
                    urls.append({
                        "loc": url,
                        "lastmod": date_published,
                        "changefreq": "monthly",
                        "priority": "0.8"
                    })

    return urls


@app.get("/sitemap.xml", response_class=PlainTextResponse)
async def sitemap_xml():
    urls = get_urls_from_json_files()

    sitemap = """<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n"""

    for url in urls:
        sitemap += f"   <url>\n"
        sitemap += f"      <loc>{url['loc']}</loc>\n"
        sitemap += f"      <lastmod>{url['lastmod']}</lastmod>\n"
        sitemap += f"      <changefreq>{url['changefreq']}</changefreq>\n"
        sitemap += f"      <priority>{url['priority']}</priority>\n"
        sitemap += f"   </url>\n"

    sitemap += "</urlset>"

    return PlainTextResponse(content=sitemap, media_type="application/xml")


@app.get("/robots.txt", response_class=FileResponse)
async def robots_txt():
    file_path = os.path.join(os.getcwd(), "robots.txt")
    return FileResponse(file_path)


app.include_router(crawler_router)
app.include_router(languages_router)
app.include_router(topics_router)
app.include_router(scraping_router)
