import requests
from bs4 import BeautifulSoup

from ai_regenerator.prompts import ai_generator_function
from bg_tasks.crawlers.Google_news_crawler.google_search_crawler import google_news_extractor
from bg_tasks.scraper.json_save import *
from bg_tasks.scraper.page_scraper import *


async def regenerate_function(soup, languages, topic, url, status):
    try:
        main_text = main_text_scraper(soup)
        img_url = img_path_scraper(soup)

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

        if main_text == "No main text found" or main_text == "Error":
            print("Main content not scrapped.")
            return {"Next_url": "This url wasn't scrapped correctly."}

        if date_published == "No date found":
            date_published = str(datetime.now())

        content_to_generate = title + " " + main_text + " " + date_published

        words = content_to_generate.split()
        word_count = len(words)

        print(word_count, "words in total.")

        # with open("scraped_urls.html", "w", encoding="utf-8") as file:
        #     file.write(str(soup))

        if status == "scrape":
            for language in languages:
                folder_prep(topic, language)
                categories = json.loads(categories_extractor(topic))

                regenerated_result = ai_generator_function(content_to_generate, language, categories)
                regenerated_result_json = json.loads(regenerated_result)

                words = regenerated_result_json["rewritten_content"].split()
                word_count = len(words)
                print(word_count, f"for {language} language.")

                json_rewritten_news_saver(regenerated_result_json, topic, language, img_url, url)

                print(f"Data appended to JSON file for {language} language.")

            save_url(url)
        else:
            print("Check data.")
            print("Title:", title)
            print("Date:", date_published)
            print("Img:", img_url)
            print("URL:", url)
            return {"Title": title, "Date": date_published, "Img": img_url, "URL": url}

    except Exception as e:
        print("Error during regenerate:", e)


async def scrape(url, topic, languages, status, bool_google=False):
    try:
        if check(url):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'
            }

            if not bool_google:
                session = requests.Session()
                session.headers.update(headers)

                response = session.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
            else:
                print("Google search.")
                soup = google_news_extractor(url)

            await regenerate_function(soup, languages, topic, url, status)

            return {"Success": "Data scraped successfully"}
        else:
            return {"Error": "URL already scraped."}

    except Exception as e:
        print(f'Error here: {e}')
        return {"Bad request": "Invalid URL or an error occurred during scraping"}
