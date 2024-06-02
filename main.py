from fastapi import FastAPI
from bg_tasks.router import router as scraping_router

app = FastAPI(
    title="News generator API",
    version="0.1"
)

app.include_router(scraping_router)
