import asyncio
import logging
from configs.config_setup import *
from bg_tasks.background_task import main_bg_function
from main_operations.crawlers.RSS_crawler.rss_crawler import show_all_topics_function

logging.basicConfig(
    filename='background_task.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


async def category_exist(name):
    try:
        list_of_cat = await show_all_topics_function()
        logging.info(f"Checked categories: {list_of_cat}")
        return name in list_of_cat
    except Exception as e:
        logging.error(f"Error checking category: {e}")
        return None


async def run_crawler(categories_list_bg, is_google=True):
    for category_name in categories_list_bg:
        logging.info(f"Starting processing for category: {category_name}")
        try:
            exists = await category_exist(category_name)
            if exists:
                logging.info(f"Category '{category_name}' exists. Starting background task.")
                try:
                    await asyncio.wait_for(main_bg_function(category_name, is_google),
                                           timeout=300.0)  # await main_bg_function(category_name, is_google)
                    logging.info(f"Background task completed for category: {category_name}")
                except Exception as e:
                    logging.error(f"Error during background task for category '{category_name}': {e}")
            else:
                logging.warning(f"Category '{category_name}' doesn't exist. Configure it in config.py")
        except Exception as e:
            logging.error(f"Error checking or processing category '{category_name}': {e}")
        finally:
            logging.info(f"Finished processing for category: {category_name}")

if __name__ == "__main__":
    logging.info("Starting background tasks...")
    try:
        asyncio.run(run_crawler(dict_of_tasks))
    except Exception as e:
        logging.critical(f"Critical error running the crawler: {e}")
    finally:
        logging.info("Shutting down tasks...")
        try:
            pending = asyncio.all_tasks()
            for task in pending:
                task.cancel()
                logging.debug(f"Cancelled task: {task}")
            try:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            except Exception as e:
                logging.error(f"Error shutting down tasks: {e}")
            finally:
                logging.info("All tasks completed and event loop closed.")
        except Exception as e:
            logging.error(f"Error cancelling task: {e}")
