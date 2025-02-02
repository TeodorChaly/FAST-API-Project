import datetime
import logging

import httpx

from configs.config_setup import main_site_topic
from main_operations.crawlers.Google_news_crawler.google_search_crawler import google_news_extractor
from main_operations.crawlers.RSS_crawler.json_save import process_json
from main_operations.scraper.json_save import *
from main_operations.scraper.page_scraper import *

logging.getLogger("httpx").setLevel(logging.WARNING)


async def regenerate_again(content_to_generate, language, categories):
    tries_count = 1
    while tries_count < 3:
        try:
            print(1431443)
            regenerated_result = await ai_generator_function(content_to_generate, language, categories, main_site_topic)
            regenerated_result_json = json.loads(regenerated_result)
            print(f"Try {tries_count} for {language}", regenerated_result_json["url_part"])
            return regenerated_result_json
        except json.JSONDecodeError as e:
            print(f"Error during regeneration {tries_count}: {e}")
            continue
    return None


async def regenerate_function(soup, languages, topic, url, status, additional_info=None):
    try:
        main_text = main_content_download(url)
        main_text_with_url = add_links_to_text(main_text, soup)
        img_url = img_path_scraper(soup)
        img_url = save_images_local(img_url, topic)

        if img_url is None:
            print("No image found.")
            return {"Next_url": "This url wasn't scrapped correctly."}

        try:
            title = title_scraper(soup)
        except Exception as e:
            print("Error during scraping title,", e)
            title = "No title"

        try:
            h1 = h1_scraper(soup)
        except Exception as e:
            print("Error during scraping title,", e)
            h1 = "No h1"
        try:
            date_published = date_published_scraper(soup)
        except Exception as e:
            print("Error during scraping date,", e)
            date_published = str(datetime.now())

        if main_text in ["No main text found", "Error"]:
            print(f"No main text found for {url}")
            return {"Next_url": "This url wasn't scrapped correctly."}

        if date_published == "No date found":
            date_published = str(datetime.now())

        try:
            additional_article_params = additional_info_scraper(soup)
        except Exception as e:
            additional_article_params = "No additional info"

        # print(await is_image_url_valid(img_url))
        # print(additional_article_params)

        content_to_generate = f"{title} | {h1} | {date_published} | {main_text} "
        word_count = len(content_to_generate.split())

        print(content_to_generate)

        print(f"{word_count} words in total.")

        if status == "scrape":
            for language in languages:
                await folder_prep(topic, language, additional_info)
                categories = json.loads(categories_extractor(topic))
                print(f"Folder prepared for {language} language.")
                regenerated_result = await ai_generator_function(content_to_generate, language, categories, topic)
                try:
                    regenerated_result_json = json.loads(regenerated_result)
                    print(f"Content for {language}", regenerated_result_json["url_part"])
                except json.JSONDecodeError as e:
                    try:
                        json_content = process_json(regenerated_result)
                        regenerated_result_json = json.loads(json_content)
                    except Exception as e2:
                        print("Mistake during regeneration. Trying again.")
                        regenerated_result_json = await regenerate_again(content_to_generate, language, categories)
                        if regenerated_result_json is None:
                            print("\n WARNING \nContent for", language, "not generated, because of\n", e2,
                                  f"\n {regenerated_result} \n")
                            continue

                if regenerated_result_json["date_published"] == "-" or regenerated_result_json["date_published"] == "":
                    regenerated_result_json["date_published"] = datetime.now().strftime("%d %m %Y %H:%M")

                await json_rewritten_news_saver(regenerated_result_json, topic, language, img_url, url)
                print(
                    f"Data appended to JSON file for {language} language with {len(regenerated_result_json['rewritten_content'].split(' '))} words.")

            await save_url(url)
        else:
            # categories = json.loads(categories_extractor(topic))
            # print(languages[0], categories)
            return {
                "URL RSS status": "correct",
                "Info": {"Title": title, "Date": date_published, "Img": img_url, "URL": url}
            }


    except Exception as e:
        print("Error during regenerate:", e)
        logging.error("Error during regenerate: %s", e, exc_info=True)

        if not os.path.exists("logs_list"):
            os.makedirs("logs_list")

        log_filename = f"logs_list/bug.log"

        with open(log_filename, "a", encoding="utf-8") as file:
            file.write(f"{str(e)}\n")


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
                async with httpx.AsyncClient(timeout=10) as client:
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
