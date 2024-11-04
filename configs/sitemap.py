import json
import os
from datetime import datetime

from fastapi import APIRouter
from starlette.responses import PlainTextResponse

from configs.config_setup import SITE_DOMAIN, main_site_topic
from content.news_file_extractor import language_to_code, get_language_name_by_code
from languages.language_json import language_json_read

router = APIRouter()


@router.get("/sitemap.xml", response_class=PlainTextResponse, tags=["Bots"])
async def sitemap_xml():
    languages = await language_json_read()

    sitemap = """<?xml version="1.0" encoding="UTF-8"?>\n"""
    sitemap += """<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n"""

    for language in languages:
        try:
            sitemap += f"   <sitemap>\n"
            sitemap += f"      <loc>{SITE_DOMAIN}/sitemap_{language_to_code(language)}.xml</loc>\n"
            sitemap += f"   </sitemap>\n"
        except Exception as e:
            print(e)

    sitemap += "</sitemapindex>"

    return PlainTextResponse(content=sitemap, media_type="application/xml")


@router.get("/sitemap_{language}.xml", response_class=PlainTextResponse, tags=["Bots"])
async def sitemap_language_xml(language: str):
    languages = await language_json_read()
    encrypted_languages = []
    for full_language in languages:
        try:
            encrypted_languages.append(language_to_code(full_language))
        except Exception as e:
            print("Not correct language", e)

    if language in encrypted_languages:
        return await sitemap_xml_function(language)
    else:
        return f"This sitemap (sitemap_{language}) not found"


def get_urls_from_json_files(language):
    full_language = get_language_name_by_code(language)
    directory = f'news_json/{main_site_topic}/'

    filepath = os.path.join(directory, f"{main_site_topic}_{full_language}.json")

    urls_list = []

    with open(filepath, 'r', encoding='utf-8') as f:
        data_list = json.load(f)
        for data in data_list:
            url_part = data.get('url_part')
            category = data.get('category')
            date_published = data.get('date_published')
            try:
                date_obj = datetime.strptime(date_published, "%d %m %Y %H:%M")
                lastmod = date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
            except Exception as e:
                lastmod = date_published

            language = data.get('language', 'en')
            language_code = language_to_code(language)

            url = f"{SITE_DOMAIN}/{language_code}/{category}/{url_part}"
            urls_list.append({
                "loc": url,
                "lastmod": lastmod,
                "changefreq": "monthly",
                "priority": "0.8"
            })

    return urls_list


async def sitemap_xml_function(language):
    xml_objects_list = get_urls_from_json_files(language)
    sitemap = """<?xml version="1.0" encoding="UTF-8"?>\n"""
    sitemap += """<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n"""

    for xml_object in xml_objects_list:
        sitemap += f"   <url>\n"
        sitemap += f"      <loc>{xml_object['loc']}</loc>\n"
        sitemap += f"      <lastmod>{xml_object['lastmod']}</lastmod>\n"
        sitemap += f"      <changefreq>{xml_object['changefreq']}</changefreq>\n"
        sitemap += f"      <priority>{xml_object['priority']}</priority>\n"
        sitemap += f"   </url>\n"

    sitemap += "</urlset>"
    return PlainTextResponse(content=sitemap, media_type="application/xml")
