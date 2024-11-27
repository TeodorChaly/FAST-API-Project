import json
import os

from main_operations.main_function import scrape
from plugin.extract_links_list import get_links


async def news_regeneration_function(topic, path, limitation=0):
    list_of_urls = await get_links("plugin/" + path, limitation)

    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    json_file_path = os.path.join(current_dir, 'languages', 'languages.json')
    with open(json_file_path, "r", encoding="utf-8") as file:
        languages = json.load(file)
    for url in list_of_urls:
        try:
            google = True
            additional_ifo = None
            print(url)
            await scrape(url, topic, languages, "scrape", google, additional_ifo)
        except Exception as e:
            print(f"Error during news regeneration: {e}")
            continue
