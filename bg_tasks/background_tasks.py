import requests
from bs4 import BeautifulSoup

from ai_regenerator.prompts import ai_generator_function
from bg_tasks.scraper.json_save import *
from bg_tasks.scraper.page_scraper import *


def regenerate_function(soup, languages, topic, url):
    title = title_scraper(soup)
    main_text = main_text_scraper(soup)
    img_url = img_path_scraper(soup)
    date_published = date_published_scraper(soup)

    if main_text == "No main text found" or main_text == "Error":
        print("Main content not scrapped.")
        return {"Next_url": "This url wasn't scrapped correctly."}

    if date_published == "No date found":
        date_published = str(datetime.now())

    content_to_generate = title + " " + main_text + " " + date_published

    words = content_to_generate.split()
    word_count = len(words)
    print(word_count)

    for language in languages:
        folder_prep(topic, language)
        categories = json.loads(categories_extractor(topic))

        regenerated_result = ai_generator_function(content_to_generate, language, categories)
        regenerated_result_json = json.loads(regenerated_result)

        words = regenerated_result_json["rewritten_content"].split()
        word_count = len(words)
        print(word_count, f"for {language} language.")

        json_rewritten_news_saver(regenerated_result_json, topic, language, img_url)

        print(f"Data appended to JSON file for {language} language.")

    save_url(url)


async def scrape(url, topic, languages):
    try:
        if check(url):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': 'https://www.example.com/',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br'
            }

            session = requests.Session()
            session.headers.update(headers)

            response = session.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            regenerate_function(soup, languages, topic, url)

            return {"Success": "Data scraped successfully"}
        else:
            return {"Error": "URL already scraped."}

    except Exception as e:
        print(f'Error here: {e}')
        return {"Bad request": "Invalid URL or an error occurred during scraping"}
