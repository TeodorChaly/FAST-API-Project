import json
import os
from urllib.parse import urlparse

import feedparser


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
        if len(new_links) < 10:
            print(f'New lists:')
            for link in new_links:
                print(link)
        else:
            print("Big list of new news.")

    return len(new_links)
