import time

from bg_tasks.background_task import main_bg_function
from configs.config_setup import bg_time, task_name, task_google

print("Starting background task.")
while True:
    time_wait = bg_time * 60
    param = task_name
    param2 = task_google
    main_bg_function(param, param2)
    time.sleep(time_wait)
