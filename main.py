import json
import os

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from main_operations.router import router as scraping_router
from topics.router import router as topics_router
from languages.router import router as languages_router
from main_operations.crawlers.RSS_crawler.router import router as crawler_router

app = FastAPI(
    title="News generator API",
    version="0.1"
)

app.mount("/static", StaticFiles(directory="templates/static"), name="static")


@app.on_event("startup")
async def startup_event():
    file_path = "languages/languages.json"
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(["english"], file)

    if not os.path.exists("scraped_urls.json"):
        with open("scraped_urls.json", 'w', encoding='utf-8') as file:
            json.dump([], file)


app.include_router(scraping_router)
app.include_router(crawler_router)
app.include_router(topics_router)
app.include_router(languages_router)


@app.post("/smart_url/{question}", tags=["Smart URL"])
def smart_url(question):
    print(question)
