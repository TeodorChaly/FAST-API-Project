import requests
import re


def add_link_to_file(link, file_name='visited_links.txt'):
    try:
        with open(file_name, 'r+') as file:
            visited_links = file.read().splitlines()

            if link not in visited_links:
                file.write(f"{link}\n")
                print(f"Link added: {link}")
            else:
                print(f"Link already was added {link}")
    except FileNotFoundError:
        with open(file_name, 'w') as file:
            file.write(f"{link}\n")

def get_final_url(url):
    response = requests.get(url)
    match = re.search(r"url:\s*'([^']+)'", response.text)
    if match:
        final_url = match.group(1)
        print(f"Final URL extracted: {final_url}")
        return final_url
    else:
        print("No redirect URL found.")
        return None

def article_content_extractor(url):
    final_url = get_final_url(url)
    if final_url:
        add_link_to_file(final_url)

        # response = requests.get(final_url)
        # print(response.text)


url = 'https://c.newsnow.co.uk/A/1245106548?-29494:15630'

article_content_extractor(url)
