from content.functions import get_categories
from content.news_file_extractor import get_language_name_by_code
from main_operations.scraper.json_save import multi_language_categories_extractor


def get_category_meta_tags(topic, category, language):
    res = multi_language_categories_extractor(topic, get_language_name_by_code(language))
    for key in res:
        if key == category:
            return key, res[key]


def get_translated_categories_name(topic, language, categories):
    main_dict = {}
    for i in categories:
        key, value = get_category_meta_tags(topic, i, language)
        main_dict[key] = value
    return main_dict


def get_translated_categories_name_and_count(topic, language, categories):
    main_dict = {}
    for category, count in categories.items():
        key, value = get_category_meta_tags(topic, category, language)
        value['count'] = count
        main_dict[key] = value
    return main_dict


async def get_header(topic, language, json_data):
    popular_categories, remaining_categories, all_categories = await get_categories(topic, json_data)

    popular_categories_dict = get_translated_categories_name(topic, language, popular_categories)
    remaining_categories_dict = get_translated_categories_name(topic, language, remaining_categories)
    return popular_categories_dict, remaining_categories_dict, all_categories

