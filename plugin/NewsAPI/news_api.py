from dotenv import load_dotenv
import requests

import os

load_dotenv()

news_api_key = os.getenv("NEWS_API_KEY")

url = 'https://newsapi.org/v2/top-headlines'
params = {
    'country': 'au',  # Новости по стране
    'category': 'business',  # Категория новостей
    'apiKey': news_api_key
}

response = requests.get(url, params=params)

for i in response.json()["articles"]:
    print(i["title"])
    print(i["description"])
    print(i["url"])
    print(i["urlToImage"])
    print(i["publishedAt"])
    print("")
print(response.text)

