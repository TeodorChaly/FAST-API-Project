import asyncio

from ai_web.web_ai import *
from ai_web.web_prompts import *


async def general_info(product):
    system_prompt = get_general_info_prompt(product)
    content, citations = await perplexity_api(product, system_prompt)
    return content, citations


async def competitors_info(product):
    system_prompt = get_competitors_info_prompt(product)
    content, citations = await perplexity_api(product, system_prompt)
    return content, citations


async def get_structure(general_content, competitors_content):
    print("General Content:", general_content)
    print("Competitors Content:", competitors_content)
    print(await get_html_structure_prompt())
    html_structure = await openai_api("test", "test")
    pass


def get_video_and_images():
    pass


async def main(topic):
    general_task = asyncio.create_task(general_info(topic))
    competitors_task = asyncio.create_task(competitors_info(topic))

    general_content, general_citations = await general_task
    competitors_content, competitors_citations = await competitors_task

    print("General Info:", general_content, general_citations)
    print("Competitors Info:", competitors_content, competitors_citations)
    await get_structure(general_content, competitors_content)


if __name__ == "__main__":
    main_topic = "example_topic"
    asyncio.run(main(main_topic))
