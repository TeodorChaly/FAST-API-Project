import feedparser
import requests
from bs4 import BeautifulSoup


def google_news_extractor():
    url = 'https://www.google.com'

    response = requests.get(url)
    cookies = response.cookies

    another_url = "https://trends.google.com/trends/trendingsearches/realtime?geo=DE&hl=en-US&category=all"
    response = requests.get(another_url, cookies=cookies)

    with open("google_search.html", "w", encoding="utf-8") as file:
        file.write(response.text)


def google_search_extractor():
    # Custom last 24 hours search

    google_search_query = "https://www.google.com/search?as_q=bitcoin&as_epq=&as_oq=&as_eq=&as_nlo=&as_nhi=&lr=&cr=countryUS&as_qdr=d&as_sitesearch=&as_occt=any&as_filetype=&tbs=#ip=1"
    headers = {
        "referer": "https://www.google.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    response = requests.get(google_search_query, headers=headers)

    with open("google_search.html", "w", encoding="utf-8") as file:
        file.write(response.text)

    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = []

    for g in soup.find_all(class_='g'):
        title = g.find('h3')
        if title:
            link = g.find('a')['href']
            snippet = g.find(class_='IsZvec')
            search_results.append({
                "title": title.get_text(),
                "link": link,
                "snippet": snippet.get_text() if snippet else ''
            })

    for result in search_results:
        print(f"Title: {result['title']}")
        print(f"Link: {result['link']}")
        print(f"Snippet: {result['snippet']}")
        print("-" * 10)


google_news_extractor()
