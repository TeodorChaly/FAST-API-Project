from dotenv import load_dotenv
import requests

import os

load_dotenv()

news_api_key = os.getenv("NEWS_API_KEY")

url = f'https://newsapi.org/v2/everything?q=Apple&apiKey={news_api_key}'

response = requests.get(url)

for i in response.json()["articles"]:
    print(i["title"])
    print(i["description"])
    print(i["url"])
    print(i["urlToImage"])
    print(i["publishedAt"])
    print("")
print(response.text)

