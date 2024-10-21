import random
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from content.functions import *
from content.news_file_extractor import *
from configs.config_setup import main_site_topic, SITE_DOMAIN, main_language, SITE_NAME

try:
    from configs.config_setup import google_id_tag
except Exception as e:
    google_id_tag = ""

from languages.language_json import languages_to_code
from main_operations.crawlers.RSS_crawler.rss_crawler import show_all_topics_function
from content.multi_language_categories import *
from main_operations.scraper.json_save import get_main_info

router = APIRouter()

templates = Jinja2Templates(directory="templates")

templates.env.filters['language_name'] = language_to_code


async def content_extractor(category, topic: str, language: str):
    try:
        language = get_language_name_by_code(language)
        file_path = f"news_json/{topic}/{topic}__terms__{language.lower()}.json"

        if os.path.isfile(file_path):
            json_result = await read_json(file_path)
            return json.loads(json_result)[category]
    except Exception as e:
        return None


async def team_extractor(topic: str, language: str):
    try:
        language = get_language_name_by_code(language)
        file_path = f"news_json/{topic}/{topic}__our_team__{language.lower()}.json"
        if os.path.isfile(file_path):
            json_result = await read_json(file_path)
            json_result = json.loads(json_result)
            return json.loads(json_result)
    except Exception as e:
        return None


async def show_content_json(topic: str, language: str = main_language, limit: int = None):
    try:
        language_name = get_language_name_by_code(language)
        return await news_extractor(topic, language_name, limit)
    except Exception:
        return "Topic or language incorrect"


@router.get("/", tags=["User content"], response_class=HTMLResponse)
async def main_page_redirect(request: Request, language: str = main_language):
    try:
        redirect = main_site_topic
        all_topic = await show_all_topics_function()

        if redirect not in all_topic:
            return f"Not correct topic {redirect}. \nGo to config_setup.py and change it. \nYou can see all topics: {all_topic}"
        else:
            return await main_page(request, topic=redirect, language=language)
    except Exception as e:
        print(e)


#
#
@router.get("/{language}", tags=["User content"], response_class=HTMLResponse)
async def main_page(request: Request, topic: str = main_site_topic, language: str = main_language, limit: int = None):
    try:
        time_now = datetime.now()
        languages = await languages_to_code()

        info_translate = get_main_info(language, topic)
        if info_translate is None:
            return templates.TemplateResponse(
                "error.html",
                {"request": request, "error": f"Invalid language."},
                status_code=404
            )

        print(f"Main page requested for {topic} in {language}.")

        json_data = await show_content_json(topic, language, limit)

        if isinstance(json_data, dict) and "error" in json_data:
            return templates.TemplateResponse(
                "error.html",
                {"request": request, "error": json_data["error"]},
                status_code=404
            )

        newest_news_len = 5
        today_news_len = 10

        popular_categories_dict, remaining_categories_dict, all_categories = await get_header(topic, language,
                                                                                              json_data)

        today_news_all = await show_content_json(topic, language, today_news_len + newest_news_len)

        newest_news = today_news_all[:newest_news_len]
        today_news = today_news_all[newest_news_len:]
        try:
            for i in newest_news:
                i["category"] = [i["category"], get_translated_categories_name(topic, language, [i["category"]])]
        except Exception as e:
            print("Newest news error", e)
        try:
            for i in today_news:
                new_category = [i["category"], get_translated_categories_name(topic, language, [i["category"]])]
                i["category"] = new_category
        except Exception as e:
            print("Today news error", e)

        content = content_all(all_categories, json_data)
        new_content = {}
        for i in content:
            new_content[get_translated_categories_name(topic, language, [i])[i]["translated_name"]] = content[i] + [
                {"category": i}]

        for i in new_content:

            for i2 in new_content[i]:
                try:
                    if i2["url_part"] == "yes":
                        pass
                except Exception as e:
                    new_content[i].remove(i2)

        try:
            footer = await content_extractor("configs", topic, language)
            if footer is None:
                footer = {
                    "config": {"about_us": "About us", "privacy_policy": "Privacy policy",
                               "terms_of_use": "Terms of use",
                               "sitemap": "Sitemap", "contact_us": "Contact us", "copyright": "copyright"},
                    "description": {"about_us": "About {SITE_NAME}",
                                    "privacy_policy": "Privacy policy of {SITE_NAME}",
                                    "terms_of_use": "Terms of use of {SITE_NAME}"}}
        except Exception as e:
            print(e)
        print(footer)
        return templates.TemplateResponse("main_page_news.html",
                                          {"request": request, "topic": topic, "language": language,
                                           "languages": languages,
                                           "top_categories": popular_categories_dict,
                                           "other_categories": remaining_categories_dict, "all_content": new_content,
                                           "today_news": today_news, "newest_news": newest_news,
                                           "info_translate": info_translate, "site_domain": SITE_DOMAIN,
                                           "site_name": SITE_NAME, "footer": footer, "google_id_tag": google_id_tag})
    except Exception as e:
        print(e, 54321)


@router.get("/{language}/{category}", tags=["User content"], response_class=HTMLResponse)
async def category_list_normal(request: Request, category: str, language: str = main_language,
                               limit: Optional[int] = None, page: int = 1, topic: str = main_site_topic):
    return await category_list(request, category, language, limit, page, topic)


@router.get("/{language}/{category}/page_{page}", tags=["User content"], response_class=HTMLResponse)
async def category_list(request: Request, category: str, language: str = main_language,
                        limit: Optional[int] = None, page: int = 1, topic: str = main_site_topic):
    try:
        language_name = get_language_name_by_code(language)
        if language_name is None:
            return templates.TemplateResponse(
                "error.html",
                {"request": request, "error": f"Invalid language."},
                status_code=404
            )
        languages_urls = await change_language_category(category, language, topic)
        print(f"Category {category} requested.")

        articles = await news_extractor(topic, language_name, limit)

        languages = await languages_to_code()

        json_data = await show_content_json(topic, language, limit)

        popular_categories_dict, remaining_categories_dict, all_categories = await get_header(topic, language,
                                                                                              json_data)
        trending_categories = get_trending_categories(all_categories)
        trending_categories_dict = get_translated_categories_name_and_count(topic, language, trending_categories)

        trending_news = await show_content_json(topic, language, 4)

        filtered_articles, total_pages = get_all_articles(articles, category, page)

        if len(filtered_articles) == 0:
            return templates.TemplateResponse(
                "error.html",
                {"request": request, "error": f"No articles found in category {category}."},
                status_code=404
            )

        about_category = get_category_meta_tags(topic, category, language)

        info_translate = get_main_info(language, topic)

        # if not filtered_articles and page == 1 or page <= 0:
        #     return templates.TemplateResponse("error.html",
        #                                       {"request": request, "error": f"No articles found in category {category}."})

        try:
            footer = await content_extractor("configs", topic, language)
            if footer is None:
                footer = {
                    "config": {"about_us": "About us", "privacy_policy": "Privacy policy",
                               "terms_of_use": "Terms of use",
                               "sitemap": "Sitemap", "contact_us": "Contact us", "copyright": "copyright"},
                    "description": {"about_us": "About {SITE_NAME}",
                                    "privacy_policy": "Privacy policy of {SITE_NAME}",
                                    "terms_of_use": "Terms of use of {SITE_NAME}"}}
        except Exception as e:
            print(e)

        try:
            team = await team_extractor(topic, language)
            list_copywriters = []
            for key, value in team.items():
                print(value["is_copywriter"])
                if value["is_copywriter"].lower() == "+":
                    list_copywriters.append(
                        {"name": value["name"], "surname": value["surname"], "image": value["image"]})
            random_copywriter = random.choice(list(list_copywriters))
        except Exception as e:
            random_copywriter = {"name": "Anna", "image": "/img/copywriters/group_1/12.jpeg"}

        return templates.TemplateResponse("category_list_template.html",
                                          {"request": request, "topic": topic, "category": category,
                                           "language": language,
                                           "articles": filtered_articles, "languages": languages,
                                           "top_categories": popular_categories_dict,
                                           "other_categories": remaining_categories_dict,
                                           "trending_categories": trending_categories_dict,
                                           "trending_news": trending_news,
                                           "page": page, "total_pages": total_pages, "about_category": about_category,
                                           "info_translate": info_translate, "site_domain": SITE_DOMAIN,
                                           "site_name": SITE_NAME, "languages_urls": languages_urls, "footer": footer,
                                           "random_copywriter": random_copywriter, "google_id_tag": google_id_tag})
    except Exception as e:
        print(e, 7654)
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": f"Category was not found."},
            status_code=404
        )


@router.get("/{language}/{category}/{url_part}", tags=["User content"], response_class=HTMLResponse)
async def article_detail(request: Request, url_part: str, language: str, category: str, topic: str = main_site_topic):
    try:
        print(f"Article {url_part} {category} requested .")

        language_name = get_language_name_by_code(language)
        if language_name is None:
            return templates.TemplateResponse("error.html", {"request": request, "error": "Invalid language."})
        articles = load_articles_from_json(topic, language_name)
        languages = await languages_to_code()

        json_data = await show_content_json(topic, language, None)
        popular_categories, remaining_categories, all_categories = await get_header(topic, language, json_data)

        trending_categories = get_trending_categories(all_categories)
        trending_categories_dict = get_translated_categories_name_and_count(topic, language, trending_categories)
        info_translate = get_main_info(language, topic)

        trending_news = await show_content_json(topic, language, 6)
        previous_and_next_news = trending_news[:4]
        previous_and_next_news_1 = previous_and_next_news[0]
        previous_and_next_news_2 = previous_and_next_news[1]
        trending_news = trending_news[2:6]
        for i in trending_news:
            i["category"] = [i["category"], get_translated_categories_name(topic, language, [i["category"]])]

        languages_dict = await change_language(url_part, language, topic)

        for article in articles:

            if article.get("url_part") == url_part and article.get("category") == category:

                author = article.get("author", "Author")
                image_path = article.get("image_path", "/img/copywriters/group_2/12.jpeg")
                copywriter = {"name": author, "image": image_path}
                print(copywriter)

                article["category"] = [article["category"],
                                       get_translated_categories_name(topic, language, [article["category"]])]
                tags = article["tags"].split(",")
                date_published = article["date_published"]
                try:
                    date_obj = datetime.strptime(date_published, "%d %m %Y %H:%M")
                    correct_time = date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
                except Exception as e:
                    correct_time = date_published

                footer_template = {
                    "config": {"about_us": "About us", "privacy_policy": "Privacy policy",
                               "terms_of_use": "Terms of use",
                               "sitemap": "Sitemap", "contact_us": "Contact us", "copyright": "copyright"},
                    "description": {"about_us": "About {SITE_NAME}",
                                    "privacy_policy": "Privacy policy of {SITE_NAME}",
                                    "terms_of_use": "Terms of use of {SITE_NAME}"}}
                try:
                    footer = await content_extractor("configs", topic, language)
                    if footer is None:
                        footer = footer_template
                except Exception as e:
                    footer = footer_template
                    print(e)

                return templates.TemplateResponse("article-details.html",
                                                  {"request": request, "topic": topic, "article": article,
                                                   "language": language, "languages": languages,
                                                   "top_categories": popular_categories,
                                                   "other_categories": remaining_categories,
                                                   "trending_categories": trending_categories_dict,
                                                   "trending_news": trending_news, "tags": tags,
                                                   "previous_and_next_news": previous_and_next_news,
                                                   "previous_and_next_news_1": previous_and_next_news_1,
                                                   "previous_and_next_news_2": previous_and_next_news_2,
                                                   "author": author, "correct_time": correct_time,
                                                   "info_translate": info_translate, "languages_dict": languages_dict,
                                                   "site_domain": SITE_DOMAIN, "site_name": SITE_NAME,
                                                   "footer": footer, "copywriter": copywriter,
                                                   "google_id_tag": google_id_tag})
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": f"No articles found with url part {url_part} in category {category}."},
            status_code=404
        )
    except Exception as e:
        print(e)
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": f"No articles found."},
            status_code=404
        )


async def change_language_category(category: str, language: str, topic: str = main_site_topic):
    try:
        language_dict = {}
        time_now = datetime.now()

        languages = await languages_to_code()

        for new_language_name in languages:
            json_response = await news_extractor(topic, get_language_name_by_code(new_language_name), None)

            for response in json_response:
                if response["category"] == category:
                    language_dict[f"{new_language_name}"] = response['category']
                    break
                else:
                    language_dict[f"{new_language_name}"] = None

        time_after = datetime.now()
        print(time_after - time_now)
        return language_dict
    except Exception as e:
        print(e)
        return {"": ""}


async def change_language(url_part: str, language: str,
                          topic: str = main_site_topic):
    try:
        language_name = get_language_name_by_code(language)
        articles = load_articles_from_json(topic, language_name)

        article = next((a for a in articles if a.get("url_part") == url_part), None)
        langauge_dict = {}

        time_now = datetime.now()
        if article:
            new_id = article.get("url")

            languages = await languages_to_code()

            for new_language_name in languages:
                json_response = await news_extractor(topic, get_language_name_by_code(new_language_name), None)
                for response in json_response:
                    if response["url"] == new_id:

                        langauge_dict[f"{new_language_name}"] = response['category'] + "/" + response['url_part']
                        break
                    else:
                        langauge_dict[f"{new_language_name}"] = None

            # print(langauge_dict)

        time_after = datetime.now()
        print(time_after - time_now)
        # print(langauge_dict, 11112)
        return langauge_dict
    except Exception as e:
        print(e)
        return {"": ""}
