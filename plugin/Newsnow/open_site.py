import requests
import re


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


url = 'https://c.newsnow.co.uk/A/1245106548?-29494:15630'

final_url = get_final_url(url)

if final_url:
    response = requests.get(final_url)
