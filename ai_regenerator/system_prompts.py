def create_prompt(text, language, list_of_categories):
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
    result2 = f"""I will give you a news text, please study it in its entirety and process it in the following JSON format and you only use this format in the same sequence:
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
    return result
