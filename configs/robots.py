from fastapi.responses import PlainTextResponse
from fastapi import APIRouter

from configs.config_setup import SITE_DOMAIN

router = APIRouter()


@router.get("/robots.txt", response_class=PlainTextResponse)
async def robots_txt():
    robots_file = f"""
User-agent: *
Disallow: /docs/
Allow: /

host: {SITE_DOMAIN}
sitemap: {SITE_DOMAIN}/sitemap.xml
"""
    return PlainTextResponse(content=robots_file)
