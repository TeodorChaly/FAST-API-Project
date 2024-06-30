import os

from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

""""Core celery task configuration"""
celery = Celery(
    "tasks",
    broker=f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}",
    include=["bg_tasks.background_task"]
)

celery.conf.beat_schedule = {
    'celery_beat_testing': {
        'task': 'bg_tasks.background_task.main_bg_function',
        'schedule': crontab(minute='*/1')
    }
}

# celery -A bg_tasks.celery_task_core beat --loglevel=info
# celery -A bg_tasks.celery_task_core worker --loglevel=info

celery.conf.timezone = 'UTC'
