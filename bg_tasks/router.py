from fastapi import Query, APIRouter
from bg_tasks.background_tasks import scrape
from languages.language_json import language_json_read

router = APIRouter(tags=["Scraping"])


@router.get("/scrape")
async def scraper_fun(url: str = Query(..., description="URL to scrape"),
                      topic: str = Query("crypto")):
    languages = language_json_read()
    result = await scrape(url, topic, languages)
    return result
