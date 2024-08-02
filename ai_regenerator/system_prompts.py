def create_prompt(language, list_of_categories):
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
            7) 'date_published': 'The date the news was published in the format 'day month year'. But if the date is not specified, you leave it -'
            8) 'author': {ai_writer_2} (and don t translate it)
            If the text contains something unrelated to the article, just skip it (and do not add it).
            The result must be only in {language} and in the correct JSON format. Here is the text of the article you need to rewrite:
        """

    return result2




