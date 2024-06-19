import requests


def google_news_extractor():
    url = 'https://www.google.com'

    response = requests.get(url)
    cookies = response.cookies

    another_url = "https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNRFJuTldzU0JXVnVMVWRDS0FBUAE?hl=en-LV&gl=LV&ceid=LV:en"
    response = requests.get(another_url, cookies=cookies)

    with open("google_search.html", "w", encoding="utf-8") as file:
        file.write(response.text)


google_news_extractor()
