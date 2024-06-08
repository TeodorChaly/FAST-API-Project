import requests
from bs4 import BeautifulSoup

from bg_tasks.scraper.json_save import *
from bg_tasks.scraper.page_scraper import *


async def scrape(url, topic, languages):
    try:
        if check(url):
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

            # Data saving (RAW NEWS)
            data = {"URL": url, "Title": title, "Main Text": main_text, "Image URL": img_url,
                    "Date Published": date_published}
            result_json_function(data, topic)

            save_url(url)

            return {"Success": "Data scraped successfully"}
        else:
            return {"Error": "URL already scraped."}

    except Exception as e:
        print(f'Error: {e}')
        return {"Bad request": "Invalid URL or an error occurred during scraping"}
