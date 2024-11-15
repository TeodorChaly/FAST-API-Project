import asyncio
import json
import os

from configs.config_setup import main_site_topic
from main_operations.main_function import scrape


async def open_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if not lines:
        print("File is empty.")

    first_line = lines[0]
    url = first_line.split(',')[0]
    print("This page is scraping", url)

    topic = main_site_topic
    google = False
    additional_ifo = None

    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_file_path = os.path.join(current_dir, 'languages', 'languages.json')
    with open(json_file_path, "r", encoding="utf-8") as file:
        languages = json.load(file)
    try:
        await scrape(url, topic, languages, "scrape", google, additional_ifo)
    except Exception as e:
        print("Error during news regeneration:", e)
        return False

    updated_lines = lines[1:]

    with open(file_path, 'w') as file:
        file.writelines(updated_lines)

    return True


if asyncio.run(open_file("list.csv")) is False:
    asyncio.run(open_file("list.csv"))
