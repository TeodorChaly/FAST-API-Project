import time
import requests
import re
from main_operations.main_function import scrape

# Make add_link_to_file async
async def add_link_to_file(link, topic, languages, file_name='visited_links.txt'):
    try:
        with open(file_name, 'r+') as file:
            visited_links = file.read().splitlines()

            if link not in visited_links:
                file.write(f"{link}\n")
                print(f"Link added: {link}")
                google = True
                additional_info = None
                # Use await inside the async function
                await scrape(link, topic, languages, "scrape", google, additional_info)
                time.sleep(2)  # If you're using async, consider replacing this with an async sleep
            else:
                print(f"Link already was added {link}")
    except FileNotFoundError:
        with open(file_name, 'w') as file:
            file.write(f"{link}\n")



def get_final_url(url):
    response = requests.get(url)
    match = re.search(r"url:\s*'([^']+)'", response.text)
    if match:
        final_url = match.group(1)
        return final_url
    else:
        return None


async def article_content_extractor(url, topic, languages):
    final_url = get_final_url(url)
    if final_url:
        await add_link_to_file(final_url, topic, languages)
