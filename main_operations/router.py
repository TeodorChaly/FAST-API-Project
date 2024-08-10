from fastapi import Query, APIRouter
from main_operations.main_function import scrape
from languages.language_json import language_json_read

router = APIRouter()


async def scraper_fun(url, topic="Crypto", google=False, additional_ifo=None):
    languages = language_json_read()
    result = await scrape(url, topic, languages, "scrape", google, additional_ifo)
    return result


@router.post("/scrape", tags=["Testing"])
async def scraper_fun_test(url: str = Query(..., description="URL to scrape"),
                           topic: str = Query("crypto"), google: bool = Query(False),
                           additional_ifo: str = Query(None, description="Additional info")):
    languages = language_json_read()
    result = await scrape(url, topic, languages, "123", google, additional_ifo)
    return result
