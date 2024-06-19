import json
import os

from fastapi import HTTPException
import aiofiles


async def add_by_rss_function(url, topic):
    if not os.path.exists("RSS_news"):
        os.makedirs("RSS_news")

    if not os.path.exists(f"RSS_news/{topic}_rss_list"):
        os.makedirs(f"RSS_news/{topic}_rss_list")

    filename = f"RSS_news/{topic}_rss_list/rss_{topic}.json"

    data = {
        "feeds": []
    }

    try:
        async with aiofiles.open(filename, 'r') as file:
            content = await file.read()
            if content:
                data = json.loads(content)
    except FileNotFoundError:
        pass

    for feed in data["feeds"]:
        if feed["url"] == url:
            raise HTTPException(status_code=400, detail="This RSS feed already exists.")

    new_feed = {
        "url": url,
        "topic": topic
    }
    data["feeds"].append(new_feed)

    async with aiofiles.open(filename, 'w') as file:
        await file.write(json.dumps(data, ensure_ascii=False, indent=4))

    return {"message": "RSS feed added successfully"}


async def extract_all_rss_function(topic):
    directory = "RSS_news"
    directory2 = f"RSS_news/{topic}_rss_list"

    if not os.path.exists(directory):
        os.makedirs(directory)

    if not os.path.exists(directory2):
        os.makedirs(directory2)

    filename = f"{directory2}/rss_{topic}.json"
    data = {
        "feeds": []
    }

    try:
        async with aiofiles.open(filename, 'r', encoding='utf-8') as file:
            content = await file.read()
            if content:
                data = json.loads(content)
                return data["feeds"]
    except FileNotFoundError:
        pass
    return data["feeds"]
