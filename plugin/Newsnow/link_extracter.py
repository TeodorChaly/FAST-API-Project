import requests
from bs4 import BeautifulSoup


from plugin.Newsnow.open_site import article_content_extractor


def scrape_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    list_of_links = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')

        for link_tag in soup.find_all('a', class_='article-card__headline'):
            link = link_tag.get('href')
            title = link_tag.text.strip()
            print(f"Link: {link}")
            list_of_links.append(link)
            article_content_extractor(link)
        print(list_of_links)
    else:
        print(f"Failed to retrieve the website. Status code: {response.status_code}")

scrape_website('https://www.newsnow.co.uk/h/Technology?type=ln')
