import json
import os


def result_json_function(scraper_result_data, content, language, url, title, main_text, img_url, date_published):
    folder_name = "news"
    file_name = f"{content}.json"
    file_path = os.path.join(folder_name, file_name)

    # Check if folder exists, create it if not
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Check if JSON file exists, create it if not
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump([], file)

    # Check if URL already exists in JSON
    with open(file_path, 'r+') as file:
        try:
            existing_data = json.load(file)
        except json.decoder.JSONDecodeError:
            existing_data = []

        urls = [item['URL'] for item in existing_data]

        if url not in urls:
            existing_data.insert(0, scraper_result_data)  # Insert new data at the beginning of the list
            file.seek(0)  # Move the file pointer to the beginning
            json.dump(existing_data, file, indent=4)
            file.truncate()  # Truncate any remaining content
            print("Data appended to JSON file.")
        else:
            print("URL already exists in JSON file. Data not appended.")

    print(f'Main text: {main_text}')
    print(f'URL: {url}')
    print(f'Title: {title}')
    print(f'Image URL: {img_url}')
    print(f'Date published: {date_published}')
