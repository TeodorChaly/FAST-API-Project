import json
import os
import logging

from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles

from main_operations.router import router as scraping_router
from content.router import router as topics_router
from languages.router import router as languages_router
from main_operations.crawlers.RSS_crawler.router import router as crawler_router

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


app.include_router(crawler_router)
app.include_router(languages_router)
app.include_router(topics_router)
app.include_router(scraping_router)
