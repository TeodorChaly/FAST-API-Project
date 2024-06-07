from fastapi import Query, APIRouter
from bg_tasks.background_tasks import scrape

router = APIRouter(tags=["Scraping"])


@router.get("/scrape")
async def scraper_fun(url: str = Query(..., description="URL to scrape"),
                      topic: str = Query("crypto"),
                      language: str = Query("english")):
    result = await scrape(url, topic, language)
    return result
