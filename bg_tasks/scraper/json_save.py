import json
import os


def result_json_function(scraper_result_data, content):
    folder_name = "news_json"
    file_name = f"{content}.json"
    file_path = os.path.join(folder_name, file_name)

    url = scraper_result_data.get('URL')

    # Check if folder exists, create it if not
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Check if JSON file exists, create it if not
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([], file)

    # Check if URL already exists in JSON
    with open(file_path, 'r+', encoding='utf-8') as file:
        try:
            existing_data = json.load(file)
        except json.decoder.JSONDecodeError:
            existing_data = []

        # Check if existing_data is not empty
        if existing_data:
            # Get the maximum existing id
            max_id = max(existing_data, key=lambda x: x.get('id', 0)).get('id', 0)
        else:
            max_id = 0

        urls = [item['URL'] for item in existing_data]

        if url not in urls:
            # Assign a new id greater than the maximum existing id
            new_id = max_id + 1
            # Add 'id' field to the scraper_result_data object
            scraper_result_data['id'] = new_id
            existing_data.insert(0, scraper_result_data)  # Insert new data at the beginning of the list
            file.seek(0)  # Move the file pointer to the beginning
            json.dump(existing_data, file, indent=4)
            file.truncate()  # Truncate any remaining content
            print("Data appended to JSON file.")
        else:
            print("URL already exists in JSON file. Data not appended.")

    # print(f'Main text: {main_text}')
    # print(f'URL: {url}')
    # print(f'Title: {title}')
    # print(f'Image URL: {img_url}')
    # print(f'Date published: {date_published}')


def check(url):
    if not os.path.exists("scraped_urls.json"):
        with open("scraped_urls.json", 'w', encoding='utf-8') as file:
            json.dump([], file)

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
