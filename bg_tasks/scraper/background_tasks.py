import requests
from bs4 import BeautifulSoup
from bg_tasks.scraper.json_save import result_json_function
from bg_tasks.scraper.page_scraper import *


async def scrape(url, content, language):
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

        data = {"URL": url, "Title": title, "Main Text": main_text, "Image URL": img_url,
                "Date Published": date_published}

        result_json_function(data, content, language, url, title, main_text, img_url, date_published)

        return {"Success": "Data scraped successfully"}

    except Exception as e:
        print(f'Error: {e}')
        return {"Bad request": "Invalid URL or an error occurred during scraping"}
