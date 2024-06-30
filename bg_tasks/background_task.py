from asgiref.sync import async_to_sync

from bg_tasks.celery_task_core import celery
from main_operations.crawlers.RSS_crawler.router import crawler_by_rss_or_feed


@celery.task(name="bg_tasks.background_task.main_bg_function")
def main_bg_function():
    param = "latvia_google_news"
    param2 = True
    async_to_sync(crawler_by_rss_or_feed)(param, param2)
    print("Time schedule unction end.")
