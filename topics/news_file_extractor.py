import json
import os


async def news_extractor(topic: str, limit):
    file_path = f"news_json/{topic}.json"

    if os.path.isfile(file_path):
        print(f"Reading JSON file: {file_path}")
        json_result = await read_json(file_path, limit)
        return json_result
    else:
        return {"error": "This topic does not exist."}


async def read_json(file_path, limit=None):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print(data)
            if limit:
                return data[:limit]
            return data
    except json.decoder.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        return []
