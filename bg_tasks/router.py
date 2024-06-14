from fastapi import Query, APIRouter
from bg_tasks.background_tasks import scrape
from bg_tasks.crawlers.json_save import rss_list_saver
from bg_tasks.crawlers.rss_crawler import *
from languages.language_json import language_json_read

router = APIRouter()


@router.post("/scrape", tags=["Scraping function"])
async def scraper_fun(url: str = Query(..., description="URL to scrape"),
                      topic: str = Query("crypto")):
    languages = language_json_read()
    result = await scrape(url, topic, languages)
    return result


@router.post("/crawler_by_RSS", tags=["RSS crawler"])
async def crawler_by_rss_or_feed(topic: str = Query(..., description="Topic")):
    list_of_urls = await extract_all_rss_function(topic)
    new_links_number = 0
    for url in list_of_urls:
        new_links_number += await rss_list_saver(url["url"], url["topic"])
    return f"RSS scraped. New - {new_links_number}"


@router.post("/add_rss_url", tags=["RSS config"])
async def add_by_rss_by_url(url: str = Query(..., description="URL to RSS"),
                            topic: str = Query(..., description="Topic")):
    return await add_by_rss_function(url, topic)


@router.get("/list_of_rss", tags=["RSS config"])
async def extract_all_rss(topic: str):
    return await extract_all_rss_function(topic)
