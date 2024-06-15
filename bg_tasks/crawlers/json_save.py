import json
import os
from urllib.parse import urlparse

import feedparser


def rss_list_saver(url, topic):
    domain = urlparse(url).netloc.replace('.', '_')

    rss_url = url

    feed = feedparser.parse(rss_url)
    new_links = []
    #
    for entry in feed.entries:
        new_links.append(entry.link)
    #
    # if not os.path.exists(f'RSS_news/{topic}_rss_sites'):
    #     os.makedirs(f'RSS_news/{topic}_rss_sites')
    # #
    # filename = f'RSS_news/{topic}_rss_sites/{domain}_rss.json'
    # max_entries = 50
    #
    # os.makedirs(os.path.dirname(filename), exist_ok=True)
    #
    # existing_links = []
    # if os.path.exists(filename):
    #     with open(filename, 'r') as f:
    #         existing_links = json.load(f)

    # Combine the new and existing links, keeping the new links first
    # combined_links = new_links + existing_links

    # Keep only unique links, preserving the order of their first appearance
    # unique_combined_links = []
    # seen_links = set()
    # for link in combined_links:
    #     if link not in seen_links:
    #         unique_combined_links.append(link)
    #         seen_links.add(link)

    # Trim the list to the maximum number of entries
    # trimmed_links = unique_combined_links[:max_entries]
    #
    # with open(filename, 'w') as f:
    #     json.dump(trimmed_links, f, indent=4)
    #
    # return new_links
    print(new_links)


rss_list_saver("https://www.cointribune.com/feed/", "r")
