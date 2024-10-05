import json
import os

from ai_regenerator.ai_api_env import API_endpoint
from ai_regenerator.system_prompts import create_prompt
from languages.language_json import language_json_read


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
                     "category2", # If you want to use two words, separate them with _ (underscore)
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
                    "translated_name":"given_category_translated to {language}", # This field must be 1-2 words and and try to use no longer than 12-14 char. 
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


async def ai_main_terms_function(json_file, topic, additional_info):
    try:
        current_file_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        folder_name = os.path.join(current_file_path, "languages")
        folder_name2 = os.path.join(folder_name, "languages.json")
        with open(folder_name2, "r", encoding="utf-8") as file:
            languages = json.load(file)
        about_us = ai_generate_about_us(languages, topic, additional_info)

        print(about_us)

        terms_json = json.loads(json_file)

        # system_fine_tuning = """
        #
        # """
        # completion = API_endpoint.chat.completions.create(
        #     model="gpt-4o-mini",
        #     messages=[
        #         {"role": "system",
        #          "content": system_fine_tuning},
        #
        #         {"role": "user", "content": "English"},
        #     ]
        # )
        # print(completion.choices[0].message.content)
        # return completion.choices[0].message.content

    except Exception as e:
        print(f'Error during generation: {e}')
        return None


async def ai_generate_about_us(SiteLanguages, SiteTheme, BriefDescription):
    try:

        prompts = f"""Craft an in-depth and engaging "About Us" section for a small but growing website. The tone should be professional, yet approachable, highlighting the unique aspects of the website while maintaining a sense of ambition and future growth. The text should appeal to the audience by showcasing the site's strengths and emphasizing its value. The focus should be on building trust, showcasing expertise, and hinting at future potential.

Details to include:
Brief Description of the Website: {BriefDescription}
Languages of the Website: {SiteLanguages}
General Theme/Focus of the Website: {SiteTheme}
The following elements must be integrated:
Introduction and Founding:

Begin by introducing the website, including when it was founded or launched. Explain what inspired the creation of the site and the core purpose behind it. The introduction should give a sense of what the site offers and why it stands out.
Multilingual Accessibility:

Highlight the fact that the website operates in {SiteLanguages}. Emphasize how this multilingual approach allows the site to cater to a diverse, global audience, making the content more accessible to people from various regions and language backgrounds.
Themes and Areas of Expertise:

Dive into the general theme or focus of the site. Clearly describe the site's main topics or areas of expertise (such as {SiteTheme}) and explain how the content is structured to provide valuable resources, articles, or services around this area. Provide examples of the type of content or resources available.
Audience and Community:

Specify who the primary audience is (e.g., individuals, businesses, professionals). Describe how the site serves their needs and provides solutions or insights that are relevant to their interests or professional goals. Touch on the growing community of readers or users who rely on the site for information, inspiration, or services.
Unique Features and Benefits:

Highlight what sets the website apart from other similar platforms. This could include a focus on quality content, a commitment to impartiality, user-friendly design, innovative tools or resources, or any specialized services. Mention any standout features that visitors can expect when using the site.
Mission and Values:

Mention the key mission of the site and its core values, such as integrity, quality, or transparency. Explain how these values guide the content creation and overall direction of the site, ensuring that the audience feels they can trust the information and services provided.
Future Ambitions and Goals:

Discuss the website’s growth trajectory and its future ambitions. This section should focus on what the website hopes to achieve, such as expanding its content offerings, reaching new audiences, or launching new features. This shows readers that the site is forward-thinking and committed to continuous improvement.
Invitation to Explore:

End with an invitation for visitors to explore the website, follow its journey, or become part of the growing community. Encourage engagement, whether it’s through subscribing, contacting the team, or sharing the content."""

        system_fine_tuning = """
        Write in English
        """
        completion = API_endpoint.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": system_fine_tuning},

                {"role": "user", "content": "Write in english"},
            ]
        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content

    except Exception as e:
        print(f'Error during generation: {e}')
        return None
