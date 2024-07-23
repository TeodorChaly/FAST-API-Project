import asyncio

from configs.config_setup import *
from bg_tasks.background_task import main_bg_function
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


def run_crawler(categories_list_bg, is_google=True):
    for category_name in categories_list_bg:
        print("-------")
        try:
            if category_exist(category_name):
                try:
                    main_bg_function(category_name, is_google)
                except Exception as e:
                    print("Error during background task:", e)
            else:
                print(f"Category '{category_name}' doesn't exist. Config it in config.py")
        except Exception as e:
            print("Error", e)
        finally:
            print()


run_crawler(dict_of_tasks)
