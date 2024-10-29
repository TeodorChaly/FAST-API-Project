import json
import os
import smtplib
from email.mime.text import MIMEText

from fastapi import APIRouter, Request, Form
from starlette.templating import Jinja2Templates

from configs.config_setup import main_site_topic, main_language, SITE_NAME
from content.multi_language_categories import get_header
from content.news_file_extractor import read_json, get_language_name_by_code
from content.router import show_content_json, content_extractor
from languages.language_json import languages_to_code
from main_operations.images_function import extract_logo_images
from main_operations.scraper.json_save import get_main_info

templates = Jinja2Templates(directory="templates")

router = APIRouter()


async def extract_translation(topic: str, language: str):
    try:
        language = get_language_name_by_code(language)
        file_path = f"news_json/{topic}/{topic}__terms__{language.lower()}.json"

        if os.path.isfile(file_path):
            json_result = await read_json(file_path)
            return json.loads(json_result)["configs"]
        else:
            return {
                'config': {'about_us': 'About us', 'privacy_policy': 'Privacy policy', 'terms_of_use': 'Terms of use',
                           'sitemap': 'Sitemap', 'contact_us': 'Contact us', 'copyright': 'copyright'}}
    except Exception as e:
        return {
            'config': {'about_us': 'About us', 'privacy_policy': 'Privacy policy', 'terms_of_use': 'Terms of use',
                       'sitemap': 'Sitemap', 'contact_us': 'Contact us', 'copyright': 'copyright'}}


async def team_extractor(topic: str, language: str):
    try:
        language = get_language_name_by_code(language)
        file_path = f"news_json/{topic}/{topic}__our_team__{language.lower()}.json"

        if os.path.isfile(file_path):
            print(file_path)
            json_result = await read_json(file_path)
            return json.loads(json_result)
    except Exception as e:
        return None


@router.get("/{language}/about_us", tags=["terms"])
async def other_content(request: Request, topic: str = main_site_topic, language: str = main_language):
    result = await content_extractor("about_us", topic, language)
    languages = await languages_to_code()
    json_data = await show_content_json(topic, language, None)
    popular_categories, remaining_categories, all_categories = await get_header(topic, language, json_data)
    info_translate = get_main_info(language, topic)
    config_translate = await extract_translation(topic, language)

    logos = await extract_logo_images()
    black_logo, white_logo = logos[0], logos[1]

    try:
        config = await content_extractor("configs", topic, language)
    except Exception as e:
        print(e)
        config = {"config": {"about_us": "About us", "privacy_policy": "Privacy policy", "terms_of_use": "Terms of use",
                             "sitemap": "Sitemap", "contact_us": "Contact us", "copyright": "copyright"},
                  "description": {"about_us": "About {SITE_NAME}",
                                  "privacy_policy": "Privacy policy of {SITE_NAME}",
                                  "terms_of_use": "Terms of use of {SITE_NAME}"}}
    if result is None:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": f"Invalid language."},
            status_code=404
        )
    else:
        return templates.TemplateResponse("footer/about_us.html",
                                          {"request": request, "topic": topic, "language": language, "content": result,
                                           "languages": languages, "top_categories": popular_categories,
                                           "other_categories": remaining_categories, "info_translate": info_translate,
                                           "footer": config, "config_translate": config_translate,
                                           "black_logo": black_logo,
                                           "white_logo": white_logo, "site_name": SITE_NAME})


@router.get("/{language}/contact_us", tags=["terms"])
async def contact_us(request: Request, topic: str = main_site_topic, language: str = main_language):
    try:
        result = await team_extractor(topic, language)
        result_dict = json.loads(result)
        config_translate = await extract_translation(topic, language)
        languages = await languages_to_code()
        json_data = await show_content_json(topic, language, None)
        popular_categories, remaining_categories, all_categories = await get_header(topic, language, json_data)
        info_translate = get_main_info(language, topic)
        config = await content_extractor("configs", topic, language)
        config_translate = await extract_translation(topic, language)

        logos = await extract_logo_images()
        black_logo, white_logo = logos[0], logos[1]

        if config is None:
            config = {
                "config": {"about_us": "About us", "privacy_policy": "Privacy policy", "terms_of_use": "Terms of use",
                           "sitemap": "Sitemap", "contact_us": "Contact us", "copyright": "copyright"},
                "description": {"about_us": "About {SITE_NAME}",
                                "privacy_policy": "Privacy policy of {SITE_NAME}",
                                "terms_of_use": "Terms of use of {SITE_NAME}"}}

        return templates.TemplateResponse("footer/contact_us.html",
                                          {"request": request, "topic": topic, "language": language,
                                           "content": result_dict,
                                           "languages": languages, "top_categories": popular_categories,
                                           "other_categories": remaining_categories, "info_translate": info_translate,
                                           "footer": config, "config_translate": config_translate,
                                           "black_logo": black_logo, "white_logo": white_logo, "site_name": SITE_NAME})
    except Exception as e:
        print(e)
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": f"Invalid language."},
            status_code=404
        )


@router.get("/{language}/privacy_policy", tags=["terms"])
async def privacy_policy(request: Request, topic: str = main_site_topic, language: str = main_language):
    result = await content_extractor("privacy_policy", topic, language)
    languages = await languages_to_code()
    json_data = await show_content_json(topic, language, None)
    popular_categories, remaining_categories, all_categories = await get_header(topic, language, json_data)
    info_translate = get_main_info(language, topic)
    config = await content_extractor("configs", topic, language)
    config_translate = await extract_translation(topic, language)

    logos = await extract_logo_images()
    black_logo, white_logo = logos[0], logos[1]

    if result is None:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": f"Invalid language."},
            status_code=404
        )
    else:
        return templates.TemplateResponse("footer/privacy_policy.html",
                                          {"request": request, "topic": topic, "language": language, "content": result,
                                           "languages": languages, "top_categories": popular_categories,
                                           "other_categories": remaining_categories, "info_translate": info_translate,
                                           "footer": config, "config_translate": config_translate,
                                           "black_logo": black_logo, "white_logo": white_logo, "site_name": SITE_NAME})


@router.get("/{language}/terms_of_use", tags=["terms"])
async def terms_of_service(request: Request, topic: str = main_site_topic, language: str = main_language):
    result = await content_extractor("terms_of_use", topic, language)
    languages = await languages_to_code()
    json_data = await show_content_json(topic, language, None)
    popular_categories, remaining_categories, all_categories = await get_header(topic, language, json_data)
    info_translate = get_main_info(language, topic)
    config = await content_extractor("configs", topic, language)
    config_translate = await extract_translation(topic, language)
    logos = await extract_logo_images()
    black_logo, white_logo = logos[0], logos[1]

    if result is None:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": f"Invalid language."},
            status_code=404
        )
    else:
        return templates.TemplateResponse("footer/terms_of_use.html",
                                          {"request": request, "topic": topic, "language": language, "content": result,
                                           "languages": languages, "top_categories": popular_categories,
                                           "other_categories": remaining_categories, "info_translate": info_translate,
                                           "footer": config, "config_translate": config_translate,
                                           "black_logo": black_logo, "white_logo": white_logo, "site_name": SITE_NAME})


@router.post("/send")
async def send_email(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    try:
        smtp_server = "smtp.office365.com"
        smtp_port = 587
        sender_email = os.getenv("GMAIL_USER")
        sender_password = os.getenv("GMAIL_PASSWORD")

        msg = MIMEText(f"Name: {name}\nEmail: {email}\nMessage:\n{message}")
        msg["Subject"] = f"New message from site {SITE_NAME}"
        msg["From"] = sender_email
        msg["To"] = sender_email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, sender_email, msg.as_string())

        return {"message": "Message sent!"}
    except Exception as e:
        return {"error": str(e)}
