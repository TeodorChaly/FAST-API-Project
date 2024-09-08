import json
import os

from languages.language_json import language_json_read
from main_operations.main_function import scrape

import asyncio


async def news_regeneration_function():
    list_of_urls = [
        "https://rus.delfi.lv/57860/latvia/120041618/opros-49-molodezhi-v-latvii-ispolzuyut-iskusstvennyy-intellekt-dlya-uchyoby-eto-bolshe-chem-v-estonii-i-litve"]

    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    json_file_path = os.path.join(current_dir, 'languages', 'languages.json')
    with open(json_file_path, "r", encoding="utf-8") as file:
        languages = json.load(file)
    for url in list_of_urls:
        topic = "latvia_google_news"
        google = True
        additional_ifo = None
        result = await scrape(url, topic, languages, "scrape", google, additional_ifo)
        return result


if __name__ == "__main__":
    asyncio.run(news_regeneration_function())
