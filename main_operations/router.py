from fastapi import Query, APIRouter, Depends, dependencies

from configs.prepare_config_file import access_required
from main_operations.main_function import scrape
from languages.language_json import language_json_read

router = APIRouter()


async def scraper_fun(url, topic, google=False, additional_ifo=None):
    languages = await language_json_read()
    result = await scrape(url, topic, languages, "scrape", google, additional_ifo)
    return result


@router.post("/scrape", tags=["Testing"])
async def scraper_fun_test(topic: str, url: str = Query(..., description="URL to scrape"),
                           api_key: dependencies = Depends(access_required)):
    languages = await language_json_read()
    result = await scrape(url, topic, languages, "scrape", False, None)
    return result
