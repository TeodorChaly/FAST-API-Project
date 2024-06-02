from fastapi import Query, APIRouter
from bg_tasks.background_tasks import scrape

router = APIRouter(tags=["Scraping"])


@router.get("/scrape")
async def scraper_fun(url: str = Query(..., description="URL to scrape")):
    await scrape(url)
    return {"message": f"Scraping initiated for {url}"}
