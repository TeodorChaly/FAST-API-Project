import time

from bg_tasks.background_task import main_bg_function

print("Starting background task.")
while True:
    time_wait = 1  # Minutes
    main_bg_function()
    time.sleep(time_wait * 60)
    print("Waiting for 60 seconds...")
