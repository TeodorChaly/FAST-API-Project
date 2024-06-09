import json
import os


def json_rewritten_news_saver(generated_json_data, topic, language, image):
    try:
        language = language.lower()
        topic = topic.lower()

        generated_json_data["topic"] = topic
        generated_json_data["language"] = language
        generated_json_data["image"] = image

        current_file_path = os.path.abspath(__file__)
        main_directory = os.path.dirname((os.path.dirname(os.path.dirname(current_file_path))))

        folder_name = os.path.join(main_directory, "news_json")
        sub_folder_name = os.path.join(folder_name, topic)
        file_name = f"{topic}_{language}.json"
        file_path = os.path.join(sub_folder_name, file_name)

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        if not os.path.exists(sub_folder_name):
            os.makedirs(sub_folder_name)

        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump([], file)
                print(f"File created: {file_path}")

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


def check(url):
    try:
        with open("scraped_urls.json", "r", encoding="utf-8") as file:
            scraped_urls = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        scraped_urls = []

    if url in scraped_urls:
        return False
    else:
        return True


def save_url(url):
    try:
        with open("scraped_urls.json", "r", encoding="utf-8") as file:
            scraped_urls = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        scraped_urls = []

    scraped_urls.append(url)
    with open("scraped_urls.json", "w", encoding="utf-8") as file:
        json.dump(scraped_urls, file, indent=4)
