from fastapi import FastAPI
from bg_tasks.router import router as scraping_router
from topics.router import router as topics_router

app = FastAPI(
    title="News generator API",
    version="0.1"
)


app.include_router(scraping_router)
app.include_router(topics_router)
