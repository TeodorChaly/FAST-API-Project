import os.path
import re
import httpx


async def has_valid_scheme(url: str) -> bool:
    return re.match(r'^https?://', url) is not None


async def is_image_url(url: str) -> bool:
    if not await has_valid_scheme(url):
        return False

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            content_type = response.headers.get('Content-Type', '')
            return content_type.startswith('image/')
        except httpx.RequestError:
            return False


async def is_image_url_valid(url):
    if url and await is_image_url(url):
        img_url = url
    else:
        img_url = "https://htmlcolorcodes.com/assets/images/colors/white-color-solid-background-1920x1080.png"  # White color as stub
    return img_url


async def extract_logo_images():
    if os.path.exists("templates/assets/img/logo/text_image_black.png") and os.path.exists(
            "templates/assets/img/logo/text_image_white.png"):
        print("Logos exist")
        return ["/img/logo/text_image_black.png", "/img/logo/text_image_white.png"]
    else:
        print("Logo not exists")
        return ["/img/logo/logo.png", "/img/logo/w_logo.png"]
