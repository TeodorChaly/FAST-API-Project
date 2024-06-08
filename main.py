import json
import os

from fastapi import FastAPI
from bg_tasks.router import router as scraping_router
from topics.router import router as topics_router
from languages.router import router as languages_router

app = FastAPI(
    title="News generator API",
    version="0.1"
)


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
app.include_router(topics_router)
app.include_router(languages_router)
