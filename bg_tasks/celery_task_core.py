import os

from celery import Celery
from celery.schedules import crontab

from config import settings

celery = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=["bg_tasks.background_tasks"]
)

celery.conf.beat_schedule = {
    'celery_beat_testing': {
        'task': 'bg_tasks.background_tasks.scrape_and_save',
        'schedule': crontab(minute='*/1')
    }
}

celery.conf.timezone = 'UTC'
