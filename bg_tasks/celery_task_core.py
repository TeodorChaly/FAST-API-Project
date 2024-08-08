# Celery application setup
import os
from dotenv import load_dotenv
from celery import Celery


load_dotenv()

celery = Celery(
    "tasks",
    broker=f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}",
    include=["bg_tasks.background_task"]
)

celery.conf.beat_schedule = {
    'celery_beat_testing': {
        'task': 'bg_tasks.background_task.main_bg_function',
        'schedule': 13  # Time in seconds
    },
    # 'second_bg_task_every_15_minutes': {
    #     'task': 'bg_tasks.background_task.second_task',
    #     'schedule': 10,
    # }
}

celery.conf.timezone = 'UTC'
