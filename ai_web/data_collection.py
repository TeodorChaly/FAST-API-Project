import asyncio
import json
import random
from datetime import datetime

from ai_regenerator.system_prompts import extract_copywriters
from ai_web.get_web_media import search_youtube_video, search_image
from ai_web.web_ai import *
from ai_web.web_prompts import *
from configs.config_setup import main_site_topic
from main_operations.scraper.json_save import save_images_local, json_rewritten_news_saver, categories_extractor


async def general_info(product):
    system_prompt = get_general_info_prompt(product)
    content, citations = await perplexity_api(product, system_prompt)
    return content, citations


async def competitors_info(product):
    system_prompt = get_competitors_info_prompt(product)
    content, citations = await perplexity_api(product, system_prompt)
    return content, citations


async def get_web_content(topic):
    general_task = asyncio.create_task(general_info(topic))
    competitors_task = asyncio.create_task(competitors_info(topic))

    general_content, general_citations = await general_task
    competitors_content, competitors_citations = await competitors_task

    print("General Info:", general_content, general_citations)
    print("Competitors Info:", competitors_content, competitors_citations)

    return {"general": [general_content, general_citations],
            "competitors": [competitors_content, competitors_citations]}


async def get_structure(general_content, competitors_content):
    structure_prompt = await get_html_structure_prompt()
    web_content_prompt = await get_combine_info_prompt(general_content, competitors_content)

    html_structure_raw = await openai_api(structure_prompt, web_content_prompt)
    try:
        html_structure_json = json.loads(html_structure_raw)
    except json.JSONDecodeError:
        print("Error decoding JSON")
        html_structure_json = None

    return html_structure_json


async def get_video_and_images(html_structure_json, sub_folder):
    video_link = search_youtube_video(html_structure_json["video"])

    images = []
    for section in html_structure_json["sections"]:
        for subsection in section["subsections"]:
            if "image" in subsection:
                images.append(subsection["image"])

    image_dict = {}
    for i in images:
        searched_img = search_image(i)
        print(searched_img)
        local_img = save_images_local(searched_img, main_site_topic, sub_folder=sub_folder)
        image_dict[i] = local_img
    print({"video": video_link, "images": image_dict})
    return {"video": video_link, "images": image_dict}


async def get_result_content(html_json_content, media_content):
    rewrite_prompt = await get_new_content_prompt()

    combine_html_text = ""

    counter = 0
    for section in html_json_content["sections"]:
        for subsection in section["subsections"]:
            if "image" in subsection:
                for key, value in media_content["images"].items():
                    if subsection["image"] == key:
                        subsection["image"] = f"alt:{key}, img:{value}"

        rewrite_content = await openai_api(rewrite_prompt,
                                           "content: " + json.dumps(section))
        print(counter)
        combine_html_text += rewrite_content
        counter += 1

    return combine_html_text


def extract_embed_url(youtube_url):
    from urllib.parse import urlparse, parse_qs

    parsed_url = urlparse(youtube_url)

    if parsed_url.netloc in ("www.youtube.com", "youtube.com") and "v" in parse_qs(parsed_url.query):
        video_id = parse_qs(parsed_url.query)["v"][0]
        return f"https://www.youtube.com/embed/{video_id}"
    else:
        raise ValueError("Not correct YouTube url")


def get_article():
    topic = "technology-news"
    language = "polish"

    main_topic = "4Runner vs Land Cruiser"

    results_dict = asyncio.run(get_web_content(main_topic))
    main_info = results_dict["general"][0]
    competitors_info = results_dict["competitors"][0]

    categories = json.loads(categories_extractor(topic))

    html_structure = asyncio.run(get_structure(main_info, competitors_info))

    media_content = asyncio.run(get_video_and_images(html_structure, main_topic))

    full_html_result = asyncio.run(get_result_content(html_structure, media_content))
    print(full_html_result)

    main_content = full_html_result
    seo_title = html_structure["title"]
    seo_description = html_structure["seo_description"]
    chosen_category = "Write AI"
    tags = html_structure["tags"]
    url_part = html_structure["url_part"]
    date_published = str(datetime.now())

    list_of_copywriter = extract_copywriters(topic)

    author = list_of_copywriter[random.randint(0, len(list_of_copywriter) - 1)]
    author_name = f"{author['name']} {author['surname']}"

    video = media_content["video"]
    images = media_content["images"]

    main_content = main_content + f"""<section id="video">
      <div class="video-wrapper">
        <iframe width="560" height="315" src="{extract_embed_url(video)}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
      </div>
    </section>
    """

    img_path = author["image"]

    content = {"rewritten_content": main_content, "seo_title": seo_title,
               "seo_description": seo_description, "category": "mobile_technology",
               "tags": tags, "url_part": url_part, "date_published": date_published,
               "author": author_name, "image_path": img_path}
    asyncio.run(json_rewritten_news_saver(content, topic, language, img_path, "-"))


if __name__ == "__main__":
    topic = "technology-news"
    language = "polish"

    main_topic = "Как достать козявек из носа"
    related_keywords = []

    competitors_info = asyncio.run(competitors_info(main_topic))
    print("Competitors Info:", competitors_info)
    html_structure = asyncio.run(get_structure(main_topic, competitors_info))
    print("HTML Structure:", html_structure)
    structure_prompt = asyncio.run(get_html_structure_prompt_3_v())
    web_content_prompt = f"""
Main Topic: {main_topic}
Competitors' Structure: {competitors_info}
Keywords: {related_keywords}"""
    html_structure_raw = asyncio.run(openai_api(structure_prompt, web_content_prompt))
    print("HTML Structure Raw:", html_structure_raw)
    html_structure_json = json.loads(html_structure_raw)
    combine_html_text = ""
    audience = html_structure_json["audience"]

    for section in html_structure_json["sections"]:
        if "keywords" in section:
            keywords = section["keywords"]
        else:
            keywords = None
        system_fine_tuning = asyncio.run(get_perplexity_prompt(main_topic, section, keywords))
        content, citations = asyncio.run(perplexity_api(system_fine_tuning, "-"))
        print("Content:", content)
        rewrite_content = asyncio.run(rewrite_content_prompt_v2(audience))

        rewrite_content = asyncio.run(openai_api(rewrite_content, content))
        print("Rewrite Content:", rewrite_content)
        combine_html_text += rewrite_content

    date_published = str(datetime.now())

    list_of_copywriter = extract_copywriters(topic)

    author = list_of_copywriter[random.randint(0, len(list_of_copywriter) - 1)]
    author_name = f"{author['name']} {author['surname']}"
    img_path = author["image"]

    content = {"rewritten_content": combine_html_text, "seo_title": html_structure_json["title"],
               "seo_description": html_structure_json["seo_description"], "category": "mobile_technology",
               "tags": html_structure_json["tags"], "url_part": html_structure_json["url_part"],
               "date_published": date_published,
               "author": author_name, "image_path": img_path}
    asyncio.run(json_rewritten_news_saver(content, topic, language, img_path, "-"))
