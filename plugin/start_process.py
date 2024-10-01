import asyncio

from plugin.news_generation import news_regeneration_function

if __name__ == "__main__":
    topic = ""  # Name of topic
    path = ''  # Filename to scrape
    limitation = 0  # Limitation of scraped urls (0 - all urls)

    asyncio.run(news_regeneration_function(topic, path, limitation))
