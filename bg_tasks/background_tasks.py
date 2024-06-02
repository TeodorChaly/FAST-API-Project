import requests
from bs4 import BeautifulSoup
from bg_tasks.page_scraper import *


async def scrape(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

        session = requests.Session()
        session.headers.update(headers)

        response = session.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        title = title_scraper(soup)
        main_text = main_text_scraper(soup)
        img_url = img_path_scraper(soup)
        date_published = date_published_scraper(soup)

        print(f'Main text: {main_text}')
        print(f'URL: {url}')
        print(f'Title: {title}')
        print(f'Image URL: {img_url}')
        print(f'Date published: {date_published}')

        return {"Message:": "Scraping successful"}

    except Exception as e:
        print(f'Error: {e}')
        return
