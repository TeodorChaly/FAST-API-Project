import time

from bg_tasks.background_task import main_bg_function

print("Starting background task.")
while True:
    time_wait = 10  # Minutes
    param = "latvia_google_news"
    param2 = True
    main_bg_function(param, param2)
    time.sleep(time_wait * 60)
