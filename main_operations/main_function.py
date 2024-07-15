import datetime
import logging

import httpx
from bs4 import BeautifulSoup

from ai_regenerator.prompts import ai_generator_function
from main_operations.crawlers.Google_news_crawler.google_search_crawler import google_news_extractor
from main_operations.scraper.json_save import *
from main_operations.scraper.page_scraper import *


async def regenerate_function(soup, languages, topic, url, status, additional_info=None):
    try:
        main_text = main_text_scraper(soup)
        img_url = img_path_scraper(soup)
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            title = title_scraper(soup)
        except Exception as e:
            print("Error during scraping title,", e)
            title = "No title"
        try:
            date_published = date_published_scraper(soup)
        except Exception as e:
            print("Error during scraping date,", e)
            date_published = str(datetime.now())

        if main_text in ["No main text found", "Error"]:
            return {"Next_url": "This url wasn't scrapped correctly."}

        if date_published == "No date found":
            date_published = str(datetime.now())

        content_to_generate = f"{title} {main_text} {date_published}"
        word_count = len(content_to_generate.split())

        print(f"{word_count} words in total.")

        if status == "scrape":
            categories = json.loads(categories_extractor(topic))
            for language in languages:
                await folder_prep(topic, language, additional_info)
                print(f"Folder prepared for {language} language.")
                regenerated_result = await ai_generator_function(content_to_generate, language, categories)
                try:
                    regenerated_result_json = json.loads(regenerated_result)
                    print(f"Content for {language}", regenerated_result_json["url_part"])
                except json.JSONDecodeError as e:
                    print("\n WARNING \nContent for", language, "not generated, because of\n", e,
                          f"\n {regenerated_result} \n")
                    continue

                await json_rewritten_news_saver(regenerated_result_json, topic, language, img_url, url)
                print(f"Data appended to JSON file for {language} language.")

            await save_url(url)
        else:
            return {
                "URL RSS status": "correct",
                "Info": {"Title": title, "Date": date_published, "Img": img_url, "URL": url}
            }


    except Exception as e:
        print("Error during regenerate:", e)
        logging.error("Error during regenerate: %s", e, exc_info=True)

        if not os.path.exists("logs_list"):
            os.makedirs("logs_list")

        now_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"logs_list/bug_{now_time}.log"

        with open(log_filename, "w", encoding="utf-8") as file:
            file.write(str(e))


async def scrape(url, topic, languages, status, bool_google=False, additional_info=None):
    try:
        if check(url):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'
            }
            if not bool_google:
                print("Not Google news")
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, headers=headers)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
            else:
                print("Google news")
                soup = await google_news_extractor(url)

            await regenerate_function(soup, languages, topic, url, status, additional_info)

            return {"Success": "Data scraped successfully"}
        else:
            return {"Error": "URL already scraped."}

    except Exception as e:
        print(f'Error here: {e}')
        return {"Bad request": "Invalid URL or an error occurred during scraping"}
