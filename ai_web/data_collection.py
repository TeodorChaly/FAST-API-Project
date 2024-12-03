import asyncio
import json

from ai_web.get_web_media import search_youtube_video, search_image
from ai_web.web_ai import *
from ai_web.web_prompts import *
from configs.config_setup import main_site_topic
from main_operations.scraper.json_save import save_images_local


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
    print("General Content:", general_content)
    print("Competitors Content:", competitors_content)
    structure_prompt = await get_html_structure_prompt()
    web_content_prompt = await get_combine_info_prompt(general_content, competitors_content)

    html_structure_raw = await openai_api(structure_prompt, web_content_prompt)
    try:
        html_structure_json = json.loads(html_structure_raw)
    except json.JSONDecodeError:
        print("Error decoding JSON")
        html_structure_json = None

    print(html_structure_json)
    return html_structure_json


async def get_video_and_images(html_structure_json):
    video_link = search_youtube_video(html_structure_json["video"])

    images = []
    for section in html_structure_json["sections"]:
        for subsection in section["subsections"]:
            if "image" in subsection:
                images.append(subsection["image"])

    image_dict = {}
    for i in images:
        image_dict[i] = search_image(i)
    return {"video": video_link, "images": image_dict}


async def get_result_content(html_json_content, media_content):
    rewrite_prompt = await get_new_content_prompt()

    combine_html_text = ""

    counter = 0
    for section in html_json_content["sections"]:
        rewrite_content = await openai_api(rewrite_prompt, "content: " + json.dumps(section))
        print(counter)
        combine_html_text += rewrite_content
        counter += 1

    return combine_html_text


if __name__ == "__main__":
    main_topic = "Golf 8"
    #
    # results_dict = asyncio.run(get_web_content(main_topic))
    # main_info = results_dict["general"][0]
    # competitors_info = results_dict["competitors"][0]
    #
    # html_structure = asyncio.run(get_structure(main_info, competitors_info))
    #
    # media_content = asyncio.run(get_video_and_images(html_structure))
    # full_html_result = asyncio.run(get_result_content(html_structure, media_content))
    # print(full_html_result)
    folder = main_topic.lower().replace(" ", "_")
    print(folder)
    print(save_images_local(
        r"https://hips.hearstapps.com/hmg-prod/images/2025-toyota-4runner-limited-108-jpg-6615620b104f8.jpg?crop\u003d0.563xw:0.474xh;0.309xw,0.409xh\u0026resize\u003d1200:*",
        main_site_topic, sub_folder=main_topic))
