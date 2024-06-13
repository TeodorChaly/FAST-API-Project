from fastapi import Query, APIRouter
from bg_tasks.background_tasks import scrape
from languages.language_json import language_json_read

router = APIRouter(tags=["Scraping"])


@router.post("/scrape")
async def scraper_fun(url: str = Query(..., description="URL to scrape"),
                      topic: str = Query("crypto")):
    languages = language_json_read()
    result = await scrape(url, topic, languages)
    return result


@router.post("/scrape_by_google_key")
async def scraper_by_key(keyword: str = Query(..., description="Keywords..."), topic: str = Query("crypto")):
    languages = language_json_read()
    print(languages)
    await crawler_google_results(keyword)
    # result = await scrape(url, topic, languages)
    # return result


async def crawler_google_results(keyword):
    print(keyword)
