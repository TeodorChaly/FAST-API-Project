import asyncio

from configs.config_setup import *
from bg_tasks.background_task import main_bg_function
from main_operations.crawlers.RSS_crawler.rss_crawler import show_all_topics_function


async def category_exist(name):
    try:
        list_of_cat = await show_all_topics_function()
        return name in list_of_cat
    except Exception as e:
        print(f"Error checking category: {e}")
        return None


async def run_crawler(categories_list_bg, is_google=True):
    for category_name in categories_list_bg:
        print("-------")
        try:
            exists = await category_exist(category_name)
            if exists:
                try:
                    await main_bg_function(category_name, is_google)
                except Exception as e:
                    print("Error during background task:", e)
            else:
                print(f"Category '{category_name}' doesn't exist. Config it in config.py")
        except Exception as e:
            print("Error", e)
        finally:
            print()


if __name__ == "__main__":
    asyncio.run(run_crawler(dict_of_tasks))
