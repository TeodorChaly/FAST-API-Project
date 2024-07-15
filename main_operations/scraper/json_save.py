import json
import os
from urllib.parse import urlparse, urlunparse

from ai_regenerator.prompts import ai_category_function


def categories_extractor(topic):
    try:
        current_file_path = os.path.abspath(__file__)
        main_directory = os.path.dirname((os.path.dirname(os.path.dirname(current_file_path))))
        folder_name = os.path.join(main_directory, "news_json")
        sub_folder_name = os.path.join(folder_name, str(topic))
        file_name = f"{topic}.json"
        file_path = os.path.join(sub_folder_name, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print("Error during categories:", e)


async def folder_prep(topic, language, additional_info=None):
    try:
        current_file_path = os.path.abspath(__file__)
        main_directory = os.path.dirname((os.path.dirname(os.path.dirname(current_file_path))))

        folder_name = os.path.join(main_directory, "news_json")
        sub_folder_name = os.path.join(folder_name, str(topic))
        file_name = f"{str(topic)}_{str(language)}.json"
        file_path = os.path.join(sub_folder_name, file_name)

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        if not os.path.exists(sub_folder_name):
            category_path = os.path.join(sub_folder_name, f"{topic}.json")
            os.makedirs(sub_folder_name)
            with open(category_path, 'w', encoding='utf-8') as file:
                ai_result = await ai_category_function(topic, additional_info)
                json.dump(ai_result, file)
                print(f"File created: {category_path}")

        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump([], file)
                print(f"File created: {file_path}")
    except Exception as e:
        print(f"Error during folder preparation: {e}")
        raise "Problem"


async def json_rewritten_news_saver(generated_json_data, topic, language, image, url):
    try:
        language = language.lower()
        topic = topic.lower()

        generated_json_data["topic"] = topic
        generated_json_data["language"] = language
        generated_json_data["image"] = image
        generated_json_data["url"] = url

        current_file_path = os.path.abspath(__file__)
        main_directory = os.path.dirname((os.path.dirname(os.path.dirname(current_file_path))))

        folder_name = os.path.join(main_directory, "news_json")
        sub_folder_name = os.path.join(folder_name, topic)
        file_name = f"{topic}_{language}.json"
        file_path = os.path.join(sub_folder_name, file_name)

        with open(file_path, 'r+', encoding='utf-8') as file:
            try:
                existing_data = json.load(file)
            except json.decoder.JSONDecodeError:
                existing_data = []

            incoming_url_part = generated_json_data.get('url_part')

            if any(item.get('url_part') == incoming_url_part for item in existing_data):
                print(f"URL part '{incoming_url_part}' already exists in the JSON file.")
            else:
                existing_data.insert(0, generated_json_data)
                file.seek(0)
                json.dump(existing_data, file, ensure_ascii=False, indent=4)
                file.truncate()
    except Exception as e:
        print(f'Error during saving new content: {e}')
        raise f"Error during saving new content: {e}"


def normalize_url(url):
    parsed_url = urlparse(url)
    normalized_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
    return normalized_url


def check(url):
    try:
        with open("scraped_urls.json", "r", encoding="utf-8") as file:
            scraped_urls = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        scraped_urls = []

    normalized_url = normalize_url(url)
    normalized_scraped_urls = [normalize_url(scraped_url) for scraped_url in scraped_urls]

    if normalized_url in normalized_scraped_urls:
        return False
    else:
        return True


async def save_url(url):
    try:
        with open("scraped_urls.json", "r", encoding="utf-8") as file:
            scraped_urls = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        scraped_urls = []

    scraped_urls.append(url)
    with open("scraped_urls.json", "w", encoding="utf-8") as file:
        json.dump(scraped_urls, file, indent=4)
