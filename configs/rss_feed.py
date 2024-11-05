import json
import os
from datetime import datetime
from fastapi import APIRouter
from starlette.responses import PlainTextResponse

from configs.config_setup import SITE_DOMAIN, main_site_topic
from configs.sitemap import get_urls_from_json_files
from content.news_file_extractor import language_to_code, get_language_name_by_code
from languages.language_json import language_json_read

router = APIRouter()

@router.get("/rss.xml", response_class=PlainTextResponse, tags=["RSS"])
async def rss_feed():
    languages = await language_json_read()

    all_rss_items = []
    for language in languages:
        language_code = language_to_code(language)
        rss_items = get_urls_from_json_files(language_code)
        all_rss_items.extend(rss_items)

    rss_feed = """<?xml version="1.0" encoding="UTF-8"?>\n"""
    rss_feed += """<rss version="2.0">\n"""
    rss_feed += """   <channel>\n"""
    rss_feed += f"      <title>News {main_site_topic}</title>\n"
    rss_feed += f"      <link>{SITE_DOMAIN}</link>\n"
    rss_feed += f"      <description>News {main_site_topic} </description>\n"
    rss_feed += f"      <language>en</language>\n"
    rss_feed += f"      <lastBuildDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}</lastBuildDate>\n"

    for item in all_rss_items:
        rss_feed += "      <item>\n"
        rss_feed += f"         <title>{item['loc'].split('/')[-1]}</title>\n"
        rss_feed += f"         <link>{item['loc']}</link>\n"
        rss_feed += f"         <description>Description</description>\n"
        rss_feed += f"         <guid>{item['loc']}</guid>\n"
        rss_feed += "      </item>\n"

    rss_feed += "   </channel>\n"
    rss_feed += "</rss>"

    return PlainTextResponse(content=rss_feed, media_type="application/rss+xml")

