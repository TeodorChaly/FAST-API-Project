import io
import json
import os
import random
import string
from urllib.parse import urlparse, urlunparse

import requests
from PIL import Image, UnidentifiedImageError

from ai_regenerator.prompts import *
from configs.config_setup import SITE_DOMAIN, SITE_NAME
from content.news_file_extractor import get_language_name_by_code


def categories_extractor(topic):
    try:
        current_file_path = os.path.abspath(__file__)
        main_directory = os.path.dirname((os.path.dirname(os.path.dirname(current_file_path))))
        folder_name = os.path.join(main_directory, "news_json")
        sub_folder_name = os.path.join(folder_name, str(topic))
        file_name = f"{topic}.json"
        file_path = os.path.join(sub_folder_name, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            # print(type(file))
            return json.load(file)
    except Exception as e:
        print("Error during categories:", e)


def multi_language_categories_extractor(topic, language):
    try:
        current_file_path = os.path.abspath(__file__)
        main_directory = os.path.dirname((os.path.dirname(os.path.dirname(current_file_path))))
        folder_name = os.path.join(main_directory, "news_json")
        sub_folder_name = os.path.join(folder_name, str(topic))
        file_name = f"{topic}__category__{language}.json"
        file_path = os.path.join(sub_folder_name, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            json_formatted = json.load(file)
        return json_formatted
    except Exception as e:
        print("Error during categories:", e)


def multi_language_configs_extractor(topic, language):
    try:
        current_file_path = os.path.abspath(__file__)
        main_directory = os.path.dirname((os.path.dirname(os.path.dirname(current_file_path))))
        folder_name = os.path.join(main_directory, "news_json")
        sub_folder_name = os.path.join(folder_name, str(topic))
        file_name = f"{topic}__configs__{language}.json"
        file_path = os.path.join(sub_folder_name, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            json_formatted = json.load(file)
        return json_formatted
    except Exception as e:
        # print("Error during configs:", e)
        pass


def get_main_info(language, topic):
    try:
        name_language = get_language_name_by_code(language)
        info_translate = multi_language_configs_extractor(topic, name_language)
    except Exception as e:
        info_translate = None
        print("Error in main page info translate", e)
    return info_translate


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

        main_category_path = os.path.join(sub_folder_name, f"{topic}.json")
        if not os.path.exists(sub_folder_name):
            os.makedirs(sub_folder_name)

            with open(main_category_path, 'w', encoding='utf-8') as file:
                ai_result = await ai_category_function(topic, additional_info)
                json.dump(ai_result, file)
                print(f"File created: {main_category_path}")

        category_path = os.path.join(sub_folder_name, f"{topic}__category__{language}.json")
        if not os.path.exists(category_path):
            with open(main_category_path, 'r', encoding='utf-8') as file:
                main_categories_list = file.read()

            for i in range(3):
                rewrite_categories_json = await ai_category_for_multiple_languages(language, main_categories_list,
                                                                                   topic)
                try:
                    json.loads(rewrite_categories_json)
                    language_category_path = os.path.join(sub_folder_name, f"{topic}__category__{language}.json")
                    with open(language_category_path, 'w', encoding='utf-8') as file:
                        json.dump(json.loads(rewrite_categories_json), file)
                    break
                except json.JSONDecodeError as e:
                    print("Error during JSON decoding. Trying again.", e)
                    continue

        category_config_path = os.path.join(sub_folder_name, f"{topic}__configs__{language}.json")
        if not os.path.exists(category_config_path):
            for i in range(3):
                rewrite_categories_json = await ai_main_config_for_multiple_languages(language, topic, additional_info)
                try:
                    json.loads(rewrite_categories_json)
                    language_category_path = os.path.join(sub_folder_name, f"{topic}__configs__{language}.json")
                    with open(language_category_path, 'w', encoding='utf-8') as file:
                        json.dump(json.loads(rewrite_categories_json), file)
                    break
                except json.JSONDecodeError as e:
                    print("Error during JSON decoding. Trying again.", e)
                    continue
                # Team file

        team_origin_path = os.path.join(sub_folder_name, f"{topic}__our_team__.json")
        if not os.path.exists(team_origin_path):
            print("Team file not found. Creating new one.")

            string_team = await ai_generate_team()
            print(string_team)

            try:
                json_team = json.dumps(string_team)
                with open(team_origin_path, 'w', encoding='utf-8') as file:
                    json.dump(json_team, file)
                    print(f"File created: {team_origin_path}")
            except json.JSONDecodeError as e:
                print("Error during JSON decoding. Trying again.", e)

        team_lang_path = os.path.join(sub_folder_name, f"{topic}__our_team__{language}.json")
        if not os.path.exists(team_lang_path):
            print("Team lang file not found. Creating new one.")

            with open(team_origin_path, 'r', encoding='utf-8') as file:
                team_list = json.load(file)

            translated_info = await ai_translate_team(team_list, language)
            try:
                translated_info = json.dumps(translated_info)
                with open(team_lang_path, 'w', encoding='utf-8') as file:
                    json.dump(translated_info, file)
            except json.JSONDecodeError as e:
                print("Error during JSON decoding. Trying again.", e)

        # Terms file
        terms_origin_path = os.path.join(sub_folder_name, f"{topic}__terms.json")
        if not os.path.exists(terms_origin_path):
            print("Terms file not found. Creating new one.")

            categories = categories_extractor(topic)

            json_terms_result = await ai_main_terms_function(topic, additional_info, SITE_DOMAIN, SITE_NAME,
                                                             categories)
            try:
                json_terms_result = json.dumps(json_terms_result)
                with open(terms_origin_path, 'w', encoding='utf-8') as file:
                    json.dump(json_terms_result, file)
                    print(f"File created: {terms_origin_path}")
            except json.JSONDecodeError as e:
                print("Error during JSON decoding. Trying again.", e)

        terms_lang_path = os.path.join(sub_folder_name, f"{topic}__terms__{language}.json")
        if not os.path.exists(terms_lang_path):
            print("Terms lang file not found. Creating new one.")

            with open(terms_origin_path, 'r', encoding='utf-8') as file:
                terms_list = json.load(file)
            terms_list = json.loads(terms_list)

            configs = f"""
                        "config": {{"about_us": "About us", "privacy_policy": "Privacy policy", "terms_of_use": "Terms of use",
                                   "sitemap": "Sitemap", "contact_us": "Contact us", "copyright": "copyright"}},
                        "description": {{"about_us": "About {SITE_NAME}",
                                        "privacy_policy": "Privacy policy of {SITE_NAME}",
                                        "terms_of_use": "Terms of use of {SITE_NAME}",
                                        "contact_us": "Contact us"}}
                    """
            translated_info = await ai_translate_terms(terms_list, language)
            config_translated = await ai_translate_config(configs, language)
            try:
                config_translated = json.loads(config_translated)
                translated_info["configs"] = config_translated
                translated_info = json.dumps(translated_info)
                with open(terms_lang_path, 'w', encoding='utf-8') as file:
                    json.dump(translated_info, file)

            except Exception as e:
                print("Error during JSON decoding. Trying again.", e)
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump([], file)
                print(f"File created: {file_path}")

    except Exception as e:
        print(f"Error during folder preparation: {e}")
        raise "Problem"


# import asyncio
#
# asyncio.run(folder_prep("latvia_google_news", "russian"))
# asyncio.run(folder_prep("latvia_google_news", "english"))

def generate_random_filename(prefix="", length=10):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choices(characters, k=length))
    return f"{prefix}_{random_string}"


def extract_prefix_from_url(url):
    filename = os.path.basename(url)
    prefix = filename.split('.')[0]
    return prefix


def compress_image(image, quality, max_size):
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='WEBP', quality=quality)
    img_byte_arr.seek(0)
    return img_byte_arr


def save_images_local(url, topic, quality=85, max_size=(1024, 1024)):
    try:
        current_file_path = os.path.abspath(__file__)
        main_directory = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
        folder_name = os.path.join(main_directory, "news_json")
        reserve_directory = os.path.join(folder_name, topic)
        save_directory = os.path.join(reserve_directory, "main_images")

        response = requests.get(url, timeout=5)
        response.raise_for_status()

        os.makedirs(save_directory, exist_ok=True)

        filename = url.split('/')[-1].split('?')[0]
        base_name = os.path.splitext(filename)[0]

        with io.BytesIO(response.content) as data_stream:
            with Image.open(data_stream) as img:
                compressed_image = compress_image(img, quality, max_size)
                output_file_path = os.path.join(save_directory, f"{base_name}.webp")

                with open(output_file_path, 'wb') as f:
                    f.write(compressed_image.getvalue())

        return f"/get_images/image?topic={topic}&img={base_name}.webp"

    except requests.exceptions.RequestException as e:
        print(f"Error via loading: {e}, {url}")
        return None
    except IOError as e:
        print(f"IO error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


async def json_rewritten_news_saver(generated_json_data, topic, language, image, url):
    try:
        language = language.lower()
        topic = topic.lower()

        new_img = save_images_local(image, topic)
        generated_json_data["topic"] = topic
        generated_json_data["language"] = language
        generated_json_data["image"] = new_img
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
