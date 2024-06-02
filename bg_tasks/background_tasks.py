import requests
from bs4 import BeautifulSoup
from page_scraper import *


def scrape(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        title = title_scraper(soup)
        main_text = main_text_scraper(soup)
        img_url = img_path_scraper(soup)
        date_published = date_published_scraper(soup)

        print(f'Title: {title}')
        print(f'Main text: {main_text}')
        print(f'Image URL: {img_url}')
        print(f'Date published: {date_published}')

    except Exception as e:
        print(f'Error: {e}')
        return


url = 'https://rus.delfi.lv/57860/latvia/120029175/foto-remeslenniki-lakomstva-i-suveniry-na-yarmarke-v-etnograficheskom-muzee-tysyachi-lyudey'
scrape(url)
