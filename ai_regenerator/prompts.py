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
        return None


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
                     all object must be in lower case. Ouput must be in JSON format and  Without ```json.
                     Here is main topic:"""
        print("start")
        completion = API_endpoint.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": system_fine_tuning},

                {"role": "user", "content": topic_name},
            ]
        )

        return completion.choices[0].message.content

    except Exception as e:
        print(f'Error during generation: {e}')
        return None


async def ai_category_for_multiple_languages(language, main_list_of_categories, topic):
    try:
        system_fine_tuning = f"""I am crating news/blog site about this topic {topic}. 
                     I will give you json list and your task to create new JSON file, that looks like this:
                    {{
                    given_category: {{
                    "translated_name":"given_category_translated to {language}", # This field must be 1-2 words. 
                    "translated_category_seo_title": "given_category_seo_title_translated to {language}",  # An SEO title no longer than 50 characters without quotes, reflecting category and being engaging
                    "translated_category_seo_description": "given_category_seo_description_translated to {language}" # An SEO description no longer than 170 characters, briefly describing category
                    }}, 
                    and so on.
                    }}
                    from categories and language that i will give you. Please keep the same structure.
                    Output must be in JSON format and  Without ```json."""
        completion = API_endpoint.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": system_fine_tuning},

                {"role": "user", "content": main_list_of_categories},
            ]
        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content

    except Exception as e:
        print(f'Error during generation: {e}')
        return None


async def ai_main_config_for_multiple_languages(language, topic, additional_info=None):
    try:
        system_fine_tuning = f"""I will give you language and you tusk is to translate (or generate) this text to given langauge (but don't translate word for word, but make the meaning clear.) and save it in this json format:
         {{
            "main_page":{{
            "seo_title": "generate here SEO title about main page (list of news) in {topic} topic. And here is additional info if it is helpful - {additional_info}"
            "seo_description":"generate here SEO description about main page (list of news) in {topic} topic. And here is additional info if it is helpful - {additional_info}"
            }},
            "other":"other",
            "read_more": "read more",
            "popular":"popular",
            "more_popular_post":"More_popular_post",
            "popular_posts":"Popular Posts",
            "more_post":"More Post",
            
            
            "read_more":"Read more",
            "trending_topic": "Trending_topic",
            "home": "Home",
            "news": "News",
            "stories": "Stories",
            "popular_stories": "Popular Stories",
            "prev_post":"Prev Post",
            "next_post":"Next Post",
            "by":"By",
            "content_writer":"Content Writer",
            "content_writer_text":"Hi there, i am"
            }}
         
            Output must be in JSON format and Without ```json. Here is language"""
        completion = API_endpoint.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": system_fine_tuning},

                {"role": "user", "content": language},
            ]
        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content

    except Exception as e:
        print(f'Error during generation: {e}')
        return None

