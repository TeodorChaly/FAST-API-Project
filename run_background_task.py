import asyncio
import time

from bg_tasks.background_task import main_bg_function
from configs.config_setup import bg_time, task_name, task_google
from main_operations.crawlers.RSS_crawler.rss_crawler import show_all_topics_function


def category_exist(name):
    try:
        list_of_cat = asyncio.run(show_all_topics_function())
        if name in list_of_cat:
            return True
        else:
            return None
    except Exception as e:
        return None


print("Starting background task.")
try:
    tries = 0
    while True:
        time_wait = bg_time * 60
        param = task_name
        param2 = task_google
        if category_exist(param):
            try:
                main_bg_function(param, param2)
                tries = 0
            except Exception as e:
                tries += 1
                print("Error during background task:", e)
            time.sleep(time_wait)
            if tries > 5:
                print("Too many errors. Stopping the process.")
                break
        else:
            print("Category doesn't exist.")
            break
except Exception as e:
    print("Error", e)
    print("Process stopped")
