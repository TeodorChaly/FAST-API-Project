from fastapi import FastAPI
from bg_tasks.background_tasks import scrape_and_save

app = FastAPI()


@app.get("/")
def main_page():
    scrape_and_save.delay()
    return {"message": "Hello World"}
