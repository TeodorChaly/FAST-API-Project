import json
from ai_regenerator.ai_api_env import API_endpoint
from ai_regenerator.system_prompts import create_prompt


def json_loader():
    folder_name = "news_json"
    file_name = f"{folder_name}/crypto.json"
    with open(f"../{file_name}", 'r') as file:
        articles = json.load(file)
    return articles


async def ai_generator_function(text, language, list_of_categories):
    try:
        system_fine_tuning = create_prompt(language, list_of_categories)
        completion = API_endpoint.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": system_fine_tuning},
                {"role": "user", "content": text},
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f'Error during generation: {e}')
        raise f"Error during generation: {e}"


async def ai_category_function(topic_name, additional_info=None):
    try:
        system_fine_tuning = f"""You are creating a news/blog site.
                     And you have to create a JSON-response list, that contains from 20 sub-categories of main category
                     /topic - {topic_name}.
                     (sub-categories must cover 100% of articles of the topic {topic_name}).
                     Here is additional info about the topic it it will help you to create sub-categories:
                     {additional_info} 
                     JSON result format:
                     [
                     "category",
                     "category2", 
                     "other" # at the end necessary add category other 
                     ]
                     please try to think abstractive and use wide categories name
                     all object must be in lower case.
                     Here is main topic:"""
        print("start")
        completion = API_endpoint.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": system_fine_tuning},

                {"role": "user", "content": topic_name},
            ]
        )

        return completion.choices[0].message.content

    except Exception as e:
        print(f'Error during generation: {e}')
        raise f"Error during generation: {e}"
