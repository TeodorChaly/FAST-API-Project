from datetime import datetime

from celery import Celery
from asgiref.sync import async_to_sync
from main_operations.crawlers.RSS_crawler.router import crawler_by_rss_or_feed

celery = Celery('tasks')


@celery.task(name='bg_tasks.background_task.main_bg_function')
def main_bg_function():
    param = "latvia_google_news"
    param2 = True
    async_to_sync(crawler_by_rss_or_feed)(param, param2)
    print(f"Task ended at {datetime.now()}.")

# @celery.task(name='bg_tasks.background_task.second_task')
# def second_task():
#     param = "2_latvia_google_news"
#     param2 = True
#     async_to_sync(crawler_by_rss_or_feed)(param, param2)
#     print("2. Time schedule function end.")
