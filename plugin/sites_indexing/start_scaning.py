import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import re


def google_search(query):
    url = 'https://www.google.com/search?'

    params = {'q': query}

    full_url = url + urlencode(params)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    response = requests.get(full_url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Ошибка при выполнении запроса: {response.status_code}")
        return None


def parse_google_results(html):
    soup = BeautifulSoup(html, 'html.parser')

    result_stats = soup.find(id='result-stats')

    if result_stats:
        result_text = result_stats.get_text()

        matches = re.findall(r'\d[\d\s]*', result_text)

        cleaned_numbers = [match.replace(' ', '').replace('\xa0', ' ') for match in matches][0]

        return cleaned_numbers
    else:
        return "Not found"



try:
    with open("sites_to_check.txt", "r", encoding="utf-8") as f:
        links = [line.strip() for line in f.readlines()]
except FileNotFoundError:
    with open("sites_to_check.txt", "w", encoding="utf-8") as f:
        f.write("example.com\n")
        links = ["example.com"]
        print(links)


for site in links:
    query = f"site:{site}"
    html_content = google_search(query)

    if html_content:
        results = parse_google_results(html_content)
        print(f"Pages indexed result for {site}: {results}")
