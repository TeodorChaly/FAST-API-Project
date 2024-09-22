from fastapi import Query, APIRouter
from main_operations.main_function import scrape
from languages.language_json import language_json_read

router = APIRouter()


async def scraper_fun(url, topic, google=False, additional_ifo=None):
    languages = await language_json_read()
    result = await scrape(url, topic, languages, "scrape", google, additional_ifo)
    return result


@router.post("/scrape", tags=["Testing"])
async def scraper_fun_test(topic: str, url: str = Query(..., description="URL to scrape"),
                           google: bool = Query(False),
                           additional_ifo: str = Query(None, description="Additional info")):
    languages = await language_json_read()
    result = await scrape(url, topic, languages, "scrape", google, additional_ifo)
    return result
