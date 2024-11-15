from fastapi import APIRouter, Depends, dependencies
from fastapi.params import Query

from configs.prepare_config_file import access_required
from languages.language_json import language_json_read
from main_operations.crawlers.RSS_crawler.json_save import rss_list_saver, get_link_source
from main_operations.crawlers.RSS_crawler.rss_crawler import *
from main_operations.router import scraper_fun
from main_operations.scraper.json_save import folder_prep

router = APIRouter()


@router.get("/check_rss_url", tags=["RSS prepare"])
async def check_by_rss_by_url(url: str = Query(..., description="URL to RSS"),
                              api_key: dependencies = Depends(access_required)):
    result = await check_by_rss_by_url_function(url)
    return result


@router.get("/link_source_check", tags=["Link source check"])
async def link_source_check(url: str = Query(..., description="URL slug to delete"),
                            api_key: dependencies = Depends(access_required)):
    try:
        url_list = url.split("/")
        url1 = url_list[2]
        language = url_list[0]
        result = await get_link_source(url1, language)
    except Exception as e:
        result = f"Error: {e}"
    return result


@router.post("/create_topic", tags=["RSS prepare"])
async def create_topic(topic: str = Query(..., description="Name of topic"),
                       additional_info: str = Query(..., description="Describe the topic"),
                       api_key: dependencies = Depends(access_required)):
    languages = await language_json_read()

    for language in languages:
        await folder_prep(topic, language, additional_info)

    return f"Topic {topic} created."


@router.post("/add_rss_url", tags=["RSS prepare"])
async def add_by_rss_by_url(url: str = Query(..., description="URL to RSS"),
                            topic: str = Query(..., description="Topic"),
                            api_key: dependencies = Depends(access_required)):
    return await add_by_rss_function(url, topic)


@router.get("/list_of_rss", tags=["RSS prepare"])
async def extract_all_rss(topic: str, api_key: dependencies = Depends(access_required)):
    return await extract_all_rss_function(topic)


@router.get("/show_all_topics", tags=["Testing"])
async def show_all_topics(api_key: dependencies = Depends(access_required)):
    return await show_all_topics_function()


@router.delete("/delete_article_by_url", tags=["Articles admin"])
async def delete_article_by_url(url: str = Query(..., description="URL slug to delete"),
                                topic: str = Query(..., description="Topic"),
                                language: str = Query(..., description="Language"),
                                api_key: dependencies = Depends(access_required)):
    return await delete_article_by_url_function(url, topic, language)


@router.delete("/delete_all_article_by_url", tags=["Articles admin"])
async def delete_all_article_by_url(url: str = Query(..., description="URL slug to delete"),
                                    topic: str = Query(..., description="Topic"),
                                    language: str = Query(..., description="Language"),
                                    api_key: dependencies = Depends(access_required)):
    return await delete_all_article_by_url_function(url, topic, language)


@router.post("/crawler_by_rss", tags=["Testing"])
async def crawler_by_rss_or_feed(topic: str = Query(..., description="Topic"),
                                 api_key: dependencies = Depends(access_required)):
    try:
        google = False
        list_of_feeds = await extract_all_rss_function(topic)
        new_links_number = 0
        new_links = []
        for feed in list_of_feeds:
            results = await rss_list_saver(feed["url"], feed["topic"])
            new_links_number += len(results)
            new_links.append(results)

        counter = 0
        for urls in new_links:
            for _ in urls:
                counter += 1

        print("Counter:", counter)
        # max_counter = len(list_of_feeds) * 10
        if counter < 9:
            for urls in new_links:
                for url in urls:
                    print("New article:", google, url)
                    if google:
                        await scraper_fun(url, topic, google=True)
                    else:
                        await scraper_fun(url, topic)
        else:
            print("Too many new links. Not scraping.")
        return f"RSS scraped. New - {new_links_number}"
    except Exception as e:
        print("Error crawler by rss:", e)
