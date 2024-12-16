import os
import requests
import xml.etree.ElementTree as ET
from get_env import xml_river_key, xml_river_user


def delete_images_if_exist(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return

    files_in_folder = os.listdir(folder_path)

    image_files = [file for file in files_in_folder if file.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp"))]

    if not image_files:
        print("No images found in the folder.")
        return

    for image in image_files:
        image_path = os.path.join(folder_path, image)
        try:
            os.remove(image_path)
            print(f"Deleted: {image_path}")
        except Exception as e:
            print(f"Error deleting file {image_path}: {e}")


def get_xmlriver_list():
    query = "4Runner vs Land Cruiser Engine"
    query = query.replace(" ", "+")
    xml_url = f'https://xmlriver.com/search/xml?query={query}+&key={xml_river_key}&user={xml_river_user}&setab=images'

    response = requests.get(xml_url)

    root = ET.fromstring(response.text)

    img_urls = [doc.find('imgurl').text for doc in root.findall('.//doc')]

    download_folder = 'downloaded_images'
    delete_images_if_exist(download_folder)
    saved_image_paths = []

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    for index, img_url in enumerate(img_urls, start=1):
        images = download_image(img_url, download_folder, index)
        if images:
            saved_image_paths.append(images)


def download_image(url, folder, index):
    try:
        img_response = requests.get(url, timeout=3)
        if img_response.status_code == 200:
            filename = os.path.join(folder, f'image_{index}.jpg')
            with open(filename, 'wb') as f:
                f.write(img_response.content)
            print(f"Downloaded: {filename}")
            return filename
        else:
            print(f"Failed to download {url}")
            return None
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None


get_xmlriver_list()
