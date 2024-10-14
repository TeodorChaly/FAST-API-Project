import json
import os
import random


def create_prompt(language, list_of_categories, topic):
    result = f"""I will give you a news text, please study it in its entirety and process it in the following JSON format and you only use this format in the same sequence:
            1) 'rewritten_content': 'Please study, shorten, and then briefly rewrite this entire news in {language}. Do not translate companie's names. If you need to use special chars (like double quotes or regular quote) - use this symbol - \ (before special char).  Be concise and laconic. Write in the third person. Separate distinct thoughts or ideas clearly, each starting with a new paragraph. In any case, separate the text into paragraphs every 2-3 sentences. Divide the text into paragraphs using <p></p> tags.'
            2) 'seo_title': 'SEO title not exceeding 50 characters, without quotes, reflecting the main theme.'
            3) 'seo_description': 'SEO description not longer than 170 characters, briefly describing the content and significance of the news.'
            4) 'category': 'The category that best reflects the topic of the news. Chose only one and only from {list_of_categories}'
            5) 'tags': 'Up to 4 relevant tags and or brands separated by commas.'
            6) 'url_part': 'Short SEO URI in Latin letters.'"
            7) 'language': 'Only one language is allowed - {language}.
            8) 'date_published': 'The date the news was published in the format YYYY-MM-DD. But if the date is not specified, you leave it -'
            Output should only be in {language} (except for names) language and in JSON format.""
            """

    ai_writer_2 = "Friendly AI"
    result2 = f""""Imagine you are a professional copywriter. You have been given the task to rewrite an article (which will be provided to you later) in a way that makes it interesting and concise to read. Additionally, you can add something interesting from yourself (such as an explanation of a term or some other interesting or useful information closely related to the topic of the article). Try to make the article better than the competitors'. 
            The text (which will be provided to you later) must be completely rewritten in {language} (with the exception of the names of certain companies or brands, but name of people try to transltate). The result must be strictly in a specific JSON format and in the same sequence:
            1) 'rewritten_content': 'Here you should concisely, informatively, and interestingly rewrite the text of the article (in {language}). Write in the third person. Clearly separate individual thoughts or ideas, each of which begins with a new paragraph. Divide the text into paragraphs using <p></p> tags.'
            2) 'seo_title': 'An SEO title no longer than 50 characters without quotes, reflecting the main topic and being engaging'
            3) 'seo_description': 'An SEO description no longer than 170 characters, briefly describing the content and significance of the news.'
            4) 'category': 'The category that best reflects the topic of the news. Choose only one and only from {list_of_categories}'
            5) 'tags': 'Up to 4 relevant tags and/or brands separated by commas.'
            6) 'url_part': 'Short SEO URI in Latin letters.'
            7) 'date_published': 'leave it -'
            8) 'author': {ai_writer_2} (and don t translate it)
            If the text contains something unrelated to the article, just skip it (and do not add it).
            The result must be only in {language} and in the correct JSON format. Here is the text of the article you need to rewrite:
        """

    ai_writer_2 = "Kind AI"

    result3 = f""""Imagine you are a professional copywriter. You have been given the task to rewrite an article (which will be provided to you later) in a way that makes it interesting and concise to read. Additionally, you can add something interesting from yourself (such as an explanation of a term or some other interesting or useful information closely related to the topic of the article). 
    Main rules:
    - never rewrite an article into its original language. Only write in {language}. 
    - Try to make the article better than the competitors (or the original). 
    - The text (which will be provided to you later) must be completely rewritten in {language} with the exception of the names of certain companies or brands.
    - name of people and locations try to translate (if it is possible). 
    The result must be strictly in a specific JSON format and in the same sequence:
                1) 'rewritten_content': 'Here you should concisely, informatively, and interestingly rewrite the text of the article (in {language}). Write in the third person. Clearly separate individual thoughts or ideas, each of which begins with a new paragraph. Divide the text into paragraphs using <p></p> tags.'
                2) 'seo_title': 'An SEO title no longer than 50 characters without quotes, reflecting the main topic and being engaging'
                3) 'seo_description': 'An SEO description no longer than 170 characters, briefly describing the content and significance of the news.'
                4) 'category': 'The category that best reflects the topic of the news. Choose only one and only from {list_of_categories}'
                5) 'tags': 'Up to 4 relevant tags and/or brands separated by commas.'
                6) 'url_part': 'Short SEO URI in Latin letters.'
                7) 'date_published': 'leave it -'
                8) 'author': {ai_writer_2} (and don t translate it)
                If the text contains something unrelated to the article, just skip it (and do not add it).
                The result MUST BE ONLY IN {language} and in the correct JSON format. Here is the text of the article you need to rewrite:
            """

    ai_writer_2 = "A. I. Writer"
    result4 = f""""Imagine you're a talented copywriter tasked with rewriting an article (which will be provided later) in a way that captivates and engages readers. You're encouraged to add your own unique insights, such as explanations of terms or additional interesting information related to the topic.

    Here are the main guidelines to follow:
    - Please write exclusively in {language}, avoiding any original language for the article.
    - Strive to make your version stand out even more than the competitors or the original text.
    - Focus on incorporating relevant keywords naturally for better SEO, without overdoing it.
    - Rewrite the provided text in {language}, ensuring to keep the names of specific companies or brands unchanged.
    - When translating names of people and locations, feel free to adapt them when possible.

    Your output should be structured strictly in a specific JSON format and in this order:
    1) 'rewritten_content': 'This is where you will concisely, informatively, and engagingly rewrite the article text (in {language}). Use the third person and clearly separate individual ideas, starting each new thought with a new paragraph. Remember to use <p></p> tags for paragraph breaks.'
    2) 'seo_title': 'Create an SEO title no longer than 50 characters, without quotes, that reflects the main topic and grabs attention.'
    3) 'seo_description': 'Craft an SEO description no longer than 170 characters that succinctly describes the content and importance of the news.'
    4) 'category': 'Select the single category that best represents the topic from {list_of_categories}.'
    5) 'tags': 'Include up to 4 relevant tags and/or brands, separated by commas.'
    6) 'url_part': 'Develop a short SEO-friendly URI in Latin letters.'
    7) 'date_published': 'Leave it as -'
    8) 'author': {ai_writer_2} (do not translate this)

    If the text includes unrelated information, feel free to skip it without adding anything extra. 

    The final result must be entirely in {language} and adhere to the correct JSON format. Here’s the article you need to rewrite:
    """

    ai_writer_2 = "A. I. Content writer"
    result5 = f""""Imagine you're a talented copywriter tasked with rewriting an article (which will be provided later) in a way that captivates and engages readers while keeping the core meaning intact. Your goal is to write in a natural, conversational style that resonates with human readers and adheres to SEO best practices.

    Here are the main guidelines to follow:
    - Please write exclusively in {language}, avoiding any original language for the article.
    - Strive to make your version stand out even more than the competitors or the original text, ensuring that the overall meaning remains the same.
    - Incorporate relevant keywords seamlessly into the content to improve SEO, but ensure they flow naturally and don’t feel forced.
    - Focus on creating valuable content that answers potential readers' questions or concerns, as Google favors informative and helpful articles.
    - Rewrite the provided text in {language}, ensuring to keep the names of specific companies or brands unchanged.
    - When translating names of people and locations, feel free to adapt them when possible.

    Your output should be structured strictly in a specific JSON format and in this order:
    1) 'rewritten_content': 'This is where you will concisely, informatively, and engagingly rewrite the article text (in {language}). Use the third person and clearly separate individual ideas, starting each new thought with a new paragraph. Remember to use <p></p> tags for paragraph breaks.'
    2) 'seo_title': 'Create an SEO title no longer than 50 characters, without quotes, that reflects the main topic and grabs attention.'
    3) 'seo_description': 'Craft an SEO description no longer than 170 characters that succinctly describes the content and importance of the news, ideally including a keyword.'
    4) 'category': 'Select the single category that best represents the topic from {list_of_categories}.'
    5) 'tags': 'Include up to 4 relevant tags and/or brands, separated by commas.'
    6) 'url_part': 'Develop a short SEO-friendly URI in Latin letters.'
    7) 'date_published': 'Leave it as -'
    8) 'author': {ai_writer_2} (do not translate this)

    If the text includes unrelated information, feel free to skip it without adding anything extra.

    The final result must be entirely in {language} and adhere to the correct JSON format. Aim for a natural tone that reflects human writing, making it engaging and relatable, while preserving the original article's meaning. Here’s the article you need to rewrite:
    """

    try:
        output_result = copy_writing_prompt(language, list_of_categories, topic)
    except Exception as e:
        output_result_list = random.randint(0, 2)
        output_result = [result3, result4, result5][output_result_list]


    return output_result


def copy_writing_prompt(language, list_of_categories, topic):
    list_of_copywriter = extract_copywriters(topic)

    author = list_of_copywriter[random.randint(0, len(list_of_copywriter) - 1)]
    author_name = f"{author['name']} {author['surname']}"
    unique_future = author["feature"]
    img_path = author["image"]

    content = f""""Imagine you're a talented copywriter tasked with rewriting an article (which will be provided later) in a way that captivates and engages readers while keeping the core meaning intact. Your goal is to write in a natural, conversational style that resonates with human readers and adheres to SEO best practices.

       Here are the main guidelines to follow:
       - Please write exclusively in {language}, avoiding any original language for the article.
       - Strive to make your version stand out even more than the competitors or the original text, ensuring that the overall meaning remains the same.
       - Incorporate relevant keywords seamlessly into the content to improve SEO, but ensure they flow naturally and don’t feel forced.
       - Focus on creating valuable content that answers potential readers' questions or concerns, as Google favors informative and helpful articles.
       - Rewrite the provided text in {language}, ensuring to keep the names of specific companies or brands unchanged.
       - When translating names of people and locations, feel free to adapt them when possible.

       Your output should be structured strictly in a specific JSON format and in this order:
       1) 'rewritten_content': 'This is where you will concisely, informatively, and engagingly rewrite the article text (in {language}). Use the third person and clearly separate individual ideas, starting each new thought with a new paragraph. Remember to use <p></p> tags for paragraph breaks.'
       2) 'seo_title': 'Create an SEO title no longer than 50 characters, without quotes, that reflects the main topic and grabs attention.'
       3) 'seo_description': 'Craft an SEO description no longer than 170 characters that succinctly describes the content and importance of the news, ideally including a keyword.'
       4) 'category': 'Select the single category that best represents the topic from {list_of_categories}.'
       5) 'tags': 'Include up to 4 relevant tags and/or brands, separated by commas.'
       6) 'url_part': 'Develop a short SEO-friendly URI in Latin letters.'
       7) 'date_published': 'Leave it as -'
       8) 'author': {author_name} 
       9) 'image_path': {img_path} (keep it as it is)

       If the text includes unrelated information, feel free to skip it without adding anything extra.

       The final result must be entirely in {language} and adhere to the correct JSON format. Aim for a natural tone that reflects human writing, making it engaging and relatable, while preserving the original article's meaning. Here’s the article you need to rewrite:
       """

    return content


def extract_copywriters(topic):
    current_file_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    try:
        folder_name = os.path.join(current_file_path, "news_json")
        folder_name2 = os.path.join(folder_name, topic)
        folder_name3 = os.path.join(folder_name2, f"{topic}__our_team__.json")
        list_of_copywriters = []
        if os.path.exists(folder_name3):
            with open(folder_name3, "r", encoding='utf-8') as file:
                raw_data = file.read()
                json_f = json.loads(raw_data)
                json_f = json.loads(json_f)
                json_f = json.loads(json_f)
                for key, value in json_f.items():
                    if value["is_copywriter"].lower() == "+":
                        list_of_copywriters.append(value)
        return list_of_copywriters

    except Exception as e:
        print(e)


# print(create_prompt("russian", ["Business", "Technology", "Health", "Entertainment"], "latvian_google_news"))
