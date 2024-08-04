import io
import json
import os
import random
import string
from urllib.parse import urlparse, urlunparse

import requests
from PIL import Image, UnidentifiedImageError

from ai_regenerator.prompts import ai_category_function, ai_category_for_multiple_languages


def categories_extractor(topic):
    try:
        current_file_path = os.path.abspath(__file__)
        main_directory = os.path.dirname((os.path.dirname(os.path.dirname(current_file_path))))
        folder_name = os.path.join(main_directory, "news_json")
        sub_folder_name = os.path.join(folder_name, str(topic))
        file_name = f"{topic}.json"
        file_path = os.path.join(sub_folder_name, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            print(type(file))
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

        else:
            print(True)

        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump([], file)
                print(f"File created: {file_path}")

    except Exception as e:
        print(f"Error during folder preparation: {e}")
        raise "Problem"


def generate_random_filename(prefix="", length=10):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choices(characters, k=length))
    return f"{prefix}_{random_string}"


def extract_prefix_from_url(url):
    filename = os.path.basename(url)
    prefix = filename.split('.')[0]
    return prefix


def compress_image(image: Image.Image, quality: int, max_size: tuple) -> io.BytesIO:
    buffered = io.BytesIO()

    image.thumbnail(max_size, Image.Resampling.LANCZOS)

    image.save(buffered, format=image.format, optimize=True, quality=quality)

    buffered.seek(0)
    return buffered


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

        prefix = extract_prefix_from_url(url)
        random_filename = prefix

        temp_path = os.path.join(save_directory, random_filename)

        with open(temp_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        try:
            jpg_check = os.path.join(save_directory, f"{random_filename}.jpg")
            png_check = os.path.join(save_directory, f"{random_filename}.png")
            if os.path.exists(jpg_check) or os.path.exists(png_check):
                if os.path.exists(jpg_check):
                    result = f"/get_images/image?topic={topic}&img={random_filename}"
                    return result
                else:
                    result = f"/get_images/image?topic={topic}&img={random_filename}"
                    return result
            else:
                with Image.open(temp_path) as img:
                    img_format = img.format.lower()

                    compressed_image = compress_image(img, quality, max_size)
                    print(img_format)
                    if img_format == 'jpg':
                        compressed_path = os.path.join(save_directory, f"{random_filename}.jpg")
                        with open(compressed_path, 'wb') as f:
                            f.write(compressed_image.getvalue())
                        random_filename += ".jpg"
                    elif img_format == 'png':
                        compressed_path = os.path.join(save_directory, f"{random_filename}.png")
                        with open(compressed_path, 'wb') as f:
                            f.write(compressed_image.getvalue())
                        random_filename += ".png"
                    else:
                        compressed_path = os.path.join(save_directory, f"{random_filename}.png")
                        with open(compressed_path, 'wb') as f:
                            f.write(compressed_image.getvalue())
                        random_filename += ".png"
                        compressed_path = temp_path

            os.remove(temp_path)
            result = f"/get_images/image?topic={topic}&img={random_filename}"
            return result

        except UnidentifiedImageError:
            os.remove(temp_path)
            print(f"File not image, {url}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error via loading: {e}, {url}")
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
