import asyncio

from plugin.news_generation import news_regeneration_function

if __name__ == "__main__":
    topic = "latvia_google_news"
    path = 'test.csv'
    limitation = 0

    asyncio.run(news_regeneration_function(topic, path, limitation))
