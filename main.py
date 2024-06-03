from fastapi import FastAPI
from bg_tasks.router import router as scraping_router

app = FastAPI(
    title="News generator API",
    version="0.1"
)

app.include_router(scraping_router)


@app.get("/content/{}", tags=["Main"])
async def show_content_json(topic: str):
    print(f"Requested topic: {topic}")
    if topic == "crypto":
        return {"message": f"Content for {topic}"}
    else:
        return {"message": "Invalid topic"}
