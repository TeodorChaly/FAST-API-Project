from bg_tasks.celery_task_core import celery


@celery.task
def scrape_and_save():
    print("New headline scraped:")
