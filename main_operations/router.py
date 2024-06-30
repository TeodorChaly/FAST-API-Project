from fastapi import Query, APIRouter
from main_operations.main_function import scrape
from languages.language_json import language_json_read

router = APIRouter()


@router.post("/scrape", tags=["Scraping function"])
async def scraper_fun(url: str = Query(..., description="URL to scrape"),
                      topic: str = Query("crypto"), google: bool = Query(False)):
    languages = language_json_read()
    result = await scrape(url, topic, languages, "scrape", google)
    return result

