import json
import os
import iso639
import pycountry


async def news_extractor(topic: str, language: str, limit):
    topic = topic.lower()
    file_path = f"news_json/{topic}/{topic}_{language.lower()}.json"

    if os.path.isfile(file_path):
        print(f"Reading JSON file: {file_path}")
        json_result = await read_json(file_path, limit)
        return json_result
    else:
        return {"error": "This topic does not exist. Use existing topic and language."}


async def read_json(file_path, limit=None):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if limit:
                return data[:limit]
            return data
    except json.decoder.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        return []


def load_articles_from_json(topic: str, language: str):
    topic = topic.lower()
    file_name = f"news_json/{topic}/{topic}_{language.lower()}.json"
    with open(file_name, 'r', encoding="utf-8") as file:
        articles = json.load(file)
    return articles


def language_to_code(language):
    try:
        code = iso639.to_iso639_1(language)
        if not code:
            code = iso639.to_iso639_2(language)
        return code
    except Exception as e:
        print(f"Error during language conversion: {e}")
        return None


def get_language_name_by_code(language_code):
    try:
        language_code = language_code.lower()
        language = pycountry.languages.get(alpha_2=language_code)
        language_name = language.name.lower()
    except AttributeError:
        language_name = "Unknown Language".lower()

    if language_name == "unknown language":
        return {"error": "Invalid language."}

    return language_name


def get_list_of_categories_for_language(articles):
    category_counts = {}

    for article in articles:
        category = article["category"]
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1

    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_categories


def get_list_of_categories_for_language_2(articles, categories):
    category_count = {category: 0 for category in categories}

    for article in articles:
        if 'category' in article and article['category'] in category_count:
            category_count[article['category']] += 1

    category_count = {category: count for category, count in category_count.items() if count > 0}

    return category_count


def split_categories_by_frequency(category_count):
    sorted_categories = sorted(category_count.items(), key=lambda item: item[1], reverse=True)

    top_5_categories = [category for category, count in sorted_categories[:5]]
    remaining_categories = [category for category, count in sorted_categories[5:]]

    return top_5_categories, remaining_categories