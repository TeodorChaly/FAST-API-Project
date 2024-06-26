import json
import os
from urllib.parse import urlparse

import feedparser
import requests

from bg_tasks.router import scraper_fun


async def rss_list_saver(url, topic):
    domain = urlparse(url).netloc.replace('.', '_')

    rss_url = url

    feed = feedparser.parse(rss_url)

    unique_links = set()

    for entry in feed.entries:
        unique_links.add(entry.link)

    if not os.path.exists(f'RSS_news/{topic}_rss_sites'):
        os.makedirs(f'RSS_news/{topic}_rss_sites')

    filename = f'RSS_news/{topic}_rss_sites/{domain}_rss.json'
    max_entries = 50

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    existing_links = set()
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            existing_links = set(json.load(f))

    new_links = list(unique_links - existing_links)
    combined_links = new_links + list(existing_links)
    combined_links = combined_links[:max_entries]

    with open(filename, 'w') as f:
        json.dump(combined_links, f, indent=4)

    if new_links:
        print(f"New RSS links: {len(new_links)}.")
        if len(new_links) < 10:
            for link in new_links:
                await scraper_fun(link)
        else:
            print("Big list of new news.")

    return new_links


def test_rss(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    list1 = rss_list_saver(url, "r")
    print(requests.get(list1[0], headers=headers))

# test_rss("https://coinbold.io/feed/")
