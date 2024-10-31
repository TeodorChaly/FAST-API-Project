from datetime import datetime

from main_operations.crawlers.RSS_crawler.router import crawler_by_rss_or_feed


async def main_bg_function(param, param2):
    try:
        print(f"Task started at {datetime.now()}.")
        await crawler_by_rss_or_feed(param, param2)
        print(f"Task ended at {datetime.now()}.")
    except Exception as e:
        print(f"Error during background task: {e}")
    finally:
        print("Task finished.")
