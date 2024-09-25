import os
import json
import requests
from bs4 import BeautifulSoup
import asyncio  # Import asyncio to run async functions
from plugin.Newsnow.open_site import article_content_extractor

async def scrape_website(url, topic, languages):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    list_of_links = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')

        for link_tag in soup.find_all('a', class_='article-card__headline'):
            link = link_tag.get('href')
            title = link_tag.text.strip()
            list_of_links.append(link)

            # Await the async function
            await article_content_extractor(link, topic, languages)

        print("Process finished")
    else:
        print(f"Failed to retrieve the website. Status code: {response.status_code}")


# Load languages JSON file
topic = "latvia_google_news"
current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
json_file_path = os.path.join(current_dir, 'languages', 'languages.json')

with open(json_file_path, "r", encoding="utf-8") as file:
    languages = json.load(file)

# Run the async function using asyncio.run
asyncio.run(scrape_website('https://www.newsnow.co.uk/h/Technology?type=ln', topic, languages))
