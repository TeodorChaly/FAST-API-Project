import json

from ai_regenerator.ai_api_env import API_endpoint


def json_loader():
    folder_name = "news_json"
    file_name = f"{folder_name}/crypto.json"
    with open(f"../{file_name}", 'r') as file:
        articles = json.load(file)
    return articles


def ai_generator_function(text, language):
    try:
        words = text.split()
        word_count = len(words)
        print(word_count)
        completion = API_endpoint.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": f"""I will give you a news text, please study it in its entirety and process it in the following JSON format:
        1) 'rewritten_content': 'Please study, shorten, and then briefly rewrite this entire news in {language}. Be concise and laconic. Write in the third person. Separate distinct thoughts or ideas clearly, each starting with a new paragraph. In any case, separate the text into paragraphs every 2-3 sentences. Divide the text into paragraphs using <p></p> tags.'
        2) 'seo_title': 'SEO title not exceeding 50 characters, without quotes, reflecting the main theme.'
        3) 'seo_description': 'SEO description not longer than 170 characters, briefly describing the content and significance of the news.'
        4) 'category': 'The category that best reflects the topic of the news.'
        5) 'tags': 'Up to 4 relevant tags and or brands separated by commas.'
        6) 'url_part': 'Short SEO URI in Latin letters.'"
        7) 'language': 'Only one language is allowed - {language}.
        8) 'date_published': 'The date the news was published in the format YYYY-MM-DD. But if the date is not specified, you leave it -'
        Output must be in {language} language.""
        """},
                {"role": "user", "content": text},
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f'Error during generation: {e}')
        raise f"Error during generation: {e}"
