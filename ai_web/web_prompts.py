def get_general_info_prompt(variable):
    general_info_prompt = f"""I am gathering information for my new article on my website about {variable}. 
        Try to find from internet (as much as possible) information about {variable}. 
        Gather information that best suits of google E-E-A-T rule. 
        If possible try to get experience/opinion or something like this"""
    return general_info_prompt


def get_competitors_info_prompt(variable):
    competitors_info_prompt = f"""I am creating an article on the topic "{variable}". 
       Scan the internet and my competitors (specifically on this topic) and provide the following in one sentence/headline:
       Group common or similar topics/headlines that are covered in competitors' articles (try to find as many such topics as possible).
       Add your input on what you would include to stand out from these competitors (suggest 2-3 unique ideas for topics or headlines).
       """
    return competitors_info_prompt


def get_competitors_info_prompt_v2(variable):
    competitors_info_prompt = f"""I am creating an article on the topic "{variable}". 
       Scan the internet and my competitor's article (specifically on this topic) and provide the following in one sentence/headline:
       Group common or similar topics/headlines that are covered in competitors' articles (try to find as many such topics as possible).
       """
    return competitors_info_prompt


async def get_html_structure_prompt():
    html_structure_prompt = """
You will be provided with:

Product information.
Competitors’ structure on the same topic.
You have information about a product and the structure of competitors on the same topic.
You need to imagine that you are writing an article on this topic and you need to make the structure of the article.
Take into account the product information and the competitors.
You also deside length of the article. 
Here are the basic rules:
Be better structured than your competitors (avoid duplicate categories, ensure clarity and uniqueness)
In the content, put what I've given you and in the product information. 

JSON Structure Guidelines:

H1: The main title, tied to the topic {variable}.
H2: Subcategories (optimized based on competitors’ structure, incorporating product information).
Each subcategory must include:
An description of the subcategory’s focus. Try to get as much information as possible from the product information.
H3: Subsections, if necessary. Each subsection may include:
An explanation of the subsection’s focus. Try to get as much information as possible from the product information.
Optionally:
A table ([table]) with headers and rows for structured data (e.g., specifications, comparisons). Table may contain up to 6 rows.
Video: At the end of the article, include a [Video description] relevant to the product or topic. Maximum 7 words to describe image, bet try to keep it shorter. 
Expected Output Format (JSON):
The output must strictly follow this format:

{
  "title": "Main Title",
  "seo_description": "Brief description summarizing the article content.",
  "url_part": "slug of URL",
  tags: "tag1, tag2, tag3",
  "sections": [
    {
      "h2": "Subcategory Title",
      "description": "Brief description summarizing the subcategory with product details.",
      "subsections": [
        {
          "h3": "Subsection Title",
          "content": "Detailed explanation relevant to the subsection.",
          "table": {
            "headers": ["Column 1", "Column 2"],
            "rows": [["Data 1", "Data 2"], ["Data 3", "Data 4"]]
          }
        }
      ]
    },
    {
      "h2": "Another Subcategory",
      "description": "Another subcategory description, with concise product information.",
      "subsections": [
        {
          "h3": "Another Subsection",
          "content": "Additional information and details.",
          "table": {
            "headers": ["Feature", "Value"],
            "rows": [["Weight", "1kg"], ["Color", "Red"]]
          }
        }
      ]
    }
  ],
  "video": "Video description: A video demonstrating the product or explaining the topic."
}

without ```json and ``` at the beginning and end of the JSON structure.

"""
    return html_structure_prompt


async def get_html_structure_prompt():
    html_structure_prompt = """
You will be provided with:

Product information.
Competitors’ structure on the same topic.
You have information about a product and the structure of competitors on the same topic.
You need to imagine that you are writing an article on this topic and you need to make the structure of the article.
Take into account the product information and the competitors.
You also deside length of the article. 
Here are the basic rules:
Be better structured than your competitors (avoid duplicate categories, ensure clarity and uniqueness)
In the content, put what I've given you and in the product information. 

JSON Structure Guidelines:

H1: The main title, tied to the topic {variable}.
H2: Subcategories (optimized based on competitors’ structure, incorporating product information).
Each subcategory must include:
An description of the subcategory’s focus. Try to get as much information as possible from the product information.
H3: Subsections, if necessary. Each subsection may include:
An explanation of the subsection’s focus. Try to get as much information as possible from the product information.
Optionally:
A table ([table]) with headers and rows for structured data (e.g., specifications, comparisons). Table may contain up to 6 rows.
Video: At the end of the article, include a [Video description] relevant to the product or topic. Maximum 7 words to describe image, bet try to keep it shorter. 
Expected Output Format (JSON):
The output must strictly follow this format:

{
  "title": "Main Title",
  "seo_description": "Brief description summarizing the article content.",
  "url_part": "slug of URL",
  tags: "tag1, tag2, tag3",
  "sections": [
    {
      "h2": "Subcategory Title",
      "description": "Brief description summarizing the subcategory with product details.",
      "subsections": [
        {
          "h3": "Subsection Title",
          "content": "Detailed explanation relevant to the subsection.",
          "table": {
            "headers": ["Column 1", "Column 2"],
            "rows": [["Data 1", "Data 2"], ["Data 3", "Data 4"]]
          }
        }
      ]
    },
    {
      "h2": "Another Subcategory",
      "description": "Another subcategory description, with concise product information.",
      "subsections": [
        {
          "h3": "Another Subsection",
          "content": "Additional information and details.",
          "table": {
            "headers": ["Feature", "Value"],
            "rows": [["Weight", "1kg"], ["Color", "Red"]]
          }
        }
      ]
    }
  ],
  "video": "Video description: A video demonstrating the product or explaining the topic."
}

without ```json and ``` at the beginning and end of the JSON structure.

"""
    return html_structure_prompt


async def get_html_structure_prompt_2_v():
    structure_prompt = """
You will be provided with 3 datas. 
1 - Main topic (central idea for the article). 
2 - Competitors' structure.
3 - Keywords (optional).

You need to imagine that you are writing an article on this topic and you need to make the structure of the article.
Take into account the main topic, competitors' structure, and keywords (if provided).

Think carefully about the target audience (using the criteria I've outlined below, 
but you can add your own if you think it's appropriate) and describe it in detail and clearly - Demographics, 
Psychographics, Needs and problems, Audience goals, Tone and style of communication.

In the content, put what I've given you and in the product information. 

And now the most important thing - thinking through the structure. the first thing (based on all the information you 
received from me and thought through yourself) to determine - the article should be small (from 1 to 3 h2), medium 
(3 - 6 h2) or large (more than 6). Please think this through very carefully. 
Based on your decision, make the scheme of the article according to the following template:

JSON Structure Guidelines:

H1: The main title, tied to the topic {variable}.
H2: Create a detail information about the subtopic.
content: Detailed explanation relevant to the subtopic.
keywords: keywords to use (optional) in the content.

Expected Output Format (JSON):
The output must strictly follow this format:

{
  "title": "Main Title",
  "seo_description": "Brief description summarizing the article content.",
  "url_part": "slug of URL",
  tags: "tag1, tag2, tag3",
  "sections": [
    {
      "h2": "Subcategory Title",
      "content": "Detailed explanation relevant to the subcategory.",
    {
      "h2": "Another Subcategory",
      "content": "Another subcategory description, with concise product information.",
      "keywords": ["keyword1", "keyword2", "keyword3"] # optional
     }
  ],
  "video": "Video description: A video demonstrating the product or explaining the topic."
}

without ```json and ``` at the beginning and end of the JSON structure.
"""

    return structure_prompt


async def get_html_structure_prompt_3_v(language):
    structure_prompt = """
You will be provided with three key pieces of data:

Main Topic
Competitors' Structure
Keywords (optional)
Your task is to create a detailed and effective structure for an article based on this information.
Follow these steps carefully:

Understand the Audience
Describe the target audience in detail, considering the following:

Demographics: Who they are (age, gender, location, education, etc.).
Psychographics: Their interests, values, and behavior.
Needs and Problems: What challenges they face related to the topic.
Goals: What they aim to achieve by reading the article.
Tone and Style: What tone (formal, casual, professional) and style (informative, engaging, persuasive) will resonate with them.

Decide the Article Length (this is the most important part)
Choose the article length based on the following factors:
Topic Complexity: How deeply does the topic need to be explored?
Audience Preferences: Estimate how much information the reader needs for a clear understanding.

Article Length
Structure: 1–3 H2 sections.



Build the Structure

Use the following JSON template to create the article structure. Be sure to include SEO-friendly elements:

H1: The main title, tied to the topic.
H2 and Content: Subcategories with detailed explanations, incorporating competitor insights and relevant product information.
Keywords: integrate them naturally into the content where provided and if you think they are not relevant, just skip them.
Video Description: Suggest a relevant, short video title to search for in YouTube  # Important: description must be in English

All content must be in {language} language. 

Expected Output Format (JSON):
The output must strictly follow this format:

{
  "title": "Main Title",
  "seo_description": "Brief description summarizing the article content.",
  "url_part": "slug of URL",
  tags: "tag1, tag2, tag3",
  "sections": [
    {
      "h2": "Subcategory Title",
      "content": "Detailed explanation relevant to the subcategory.",
      "keywords": ["keyword1", "keyword2", "keyword3"] # Pest keywords (that will be provided) where you think it is suits the best
    {
      "h2": "Another Subcategory",
      "content": "Another subcategory description, with concise product information.",
      "keywords": [] # Pest keywords (that will be provided) where you think it is suits the best
     }
  ],
  "audience": "Audience description: Demographics, Psychographics, Needs and problems, Audience goals, Tone and style of communication.",
  "video": "Video description: A short video title about product or topic. # Necessary in English"
}

without ```json and ``` at the beginning and end of the JSON structure.
"""

    return structure_prompt


async def get_perplexity_prompt(main_topic, section, keywords):
    text = f"""Write a detailed explanation about the specified subtopic. 
    Simply provide comprehensive information based on the given details. 

    Main topic: {main_topic}. 
    Subtopic title: {section["h2"]}. 
    Subtopic brief description: {section["content"]}. 
    Keywords to include (if any): {keywords}.

    Important: The response must not include any conclusions, summaries, or closing statements. End the text immediately after delivering the detailed information.
    """

    return text


async def rewrite_content_prompt():
    content = f"""
      You will be provided with a text and your task is to rewrite the content in a more engaging way.
      Content must be E-E-A-T friendly and you should add something from your own experience or opinion and knowledge.
      Then you need to convert new text into an HTML block, which will then be combined with other HTML blocks. 
      The output must be valid HTML without any PHP or JavaScript code or CSS code (except inline CSS for tables).
      Try to use different keywords (but don t owerspam) and try to make the text more engaging. Try to udnerstend: 
      does this part of content must be big or small, does it need to be more detailed or less detailed (for better
       user experience). Word count may various from 40 to 1000 words.Without ```html and ``` at the beginning and end. 
     """

    return content


async def rewrite_content_prompt_v2(audience):
    content = f"""
      You will receive a text related to a specific topic. Your objective is to rewrite it with the following guidelines:

Audience Context: The target audience has the following characteristics: {audience}. Tailor your language, tone, and depth of explanation to suit this audience.

Content Structure:

Analyze the provided text to determine whether certain sections require in-depth answers with tables, bullet points, subheadings, or just brief responses. Use only the level of detail that enhances user experience.
Create a logical and intuitive structure to guide the user seamlessly through the content.
SEO & E-E-A-T Requirements:

Integrate keywords naturally (but avoid keyword stuffing). 
Prioritize Expertise, Experience, Authoritativeness, and Trustworthiness (E-E-A-T) by leveraging your knowledge, perspective, or insight when appropriate.
Personal Touch & Added Insights:

Incorporate your personal experience, opinion, or expertise when relevant, to make the text more relatable and engaging for readers.
HTML Conversion:

Format the final response as a valid HTML block. Do not use PHP, JavaScript, or CSS unless it’s inline for tables.
Ensure the text uses proper headings and semantic HTML tags to improve accessibility and SEO.
Content Formatting Instructions
The output can vary from 40 words to 1000 words, depending on the depth and context required by the prompt.
Think critically about each subtopic. Decide whether to add tables, detailed breakdowns, or short answers based on the user's experience needs.
Submission Format
After rewriting, ensure the response is formatted in standard, valid HTML only (with inline styles for tables if needed). Here’s an example of the expected format:

If there are conclusions in the provided text, please exclude them. However, if you believe they are very relevant,
present them as a summary specifically for this section (and under no circumstances should you make them h2 headings).

<h2>Subtopic Title Here</h2>
<p>Write the rewritten and engaging content here, following the SEO, E-E-A-T principles, and user intent.</p>
<table style="border: 1px solid black; width: 100%;">
  <tr>
    <th style="border: 1px solid black;">Header 1</th>
    <th style="border: 1px solid black;">Header 2</th>
  </tr>
  <tr>
    <td style="border: 1px solid black;">Row 1, Column 1</td>
    <td style="border: 1px solid black;">Row 1, Column 2</td>
  </tr>
</table>


Additional Considerations
Content Should Be:

Engaging, clear, and informative.
Scannable for users by utilizing bullet points, numbered lists, tables, and subheadings.
Written with proper grammar and tone consistency.
Audience Experience:
Always prioritize user intent. Ask yourself:

Is the information easy to digest?
Does it provide value to the reader?
Keyword Usage:

Use provided keywords naturally within the text.
Do not overuse them; instead, focus on high-quality, conversational language.

And please - Without ```html and ``` at the beginning and end of the HTML block.
"""

    return content

async def rewrite_content_prompt_4_v(audience, content_short_summary):
    structure_prompt = f"""
    You will receive a text related to a specific topic. Additionally, you will be provided with a short summary of the content, which must be considered when rewriting. 
    Your objective is to rewrite the text with the following guidelines and answer title in provided text:  

Audience Context: The target audience has the following characteristics: {audience}. Tailor your language, tone, and depth of explanation to suit this audience.  

Content Summary: Analyze the provided short summary "{content_short_summary}" and ensure that your response avoiding repetition. 

Content Structure:  
- Analyze the provided text to determine whether certain sections require in-depth answers with tables, bullet points, subheadings, or just brief responses. Use only the level of detail that enhances user experience.  
- Create a logical and intuitive structure to guide the user seamlessly through the content.  

SEO & E-E-A-T Requirements:  
- Integrate keywords naturally (but avoid keyword stuffing).  
- Prioritize Expertise, Experience, Authoritativeness, and Trustworthiness (E-E-A-T) by leveraging your knowledge, perspective, or insight when appropriate.  

Personal Touch & Added Insights:  
- Incorporate your personal experience, opinion, or expertise when relevant, to make the text more relatable and engaging for readers.  

HTML Conversion:  
- Format the final response as a valid HTML block. Do not use PHP, JavaScript, or CSS unless it’s inline for tables.  
- Ensure the text uses proper headings and semantic HTML tags to improve accessibility and SEO. 
- You could also (and it would be even better) use text formatting - say highlighting text with bolt or italics or something that will make the text more readable.

Content Formatting Instructions:  
- The output can vary from 40 words to 1000 words, depending on the depth and context required by the prompt.  
- Think critically about each subtopic. Decide whether to add tables, detailed breakdowns, or short answers based on the user's experience needs.  

Submission Format:  
After rewriting, ensure the response is formatted in standard, valid HTML only (with inline styles for tables if needed). Here’s an example of the expected format:  

<h2>Subtopic Title Here</h2>  
<p>Write the rewritten and engaging content here, following the SEO, E-E-A-T principles, and user intent.</p>  
<table style="border: 1px solid black; width: 100%;">  
  <tr>  
    <th style="border: 1px solid black;">Header 1</th>  
    <th style="border: 1px solid black;">Header 2</th>  
  </tr>  
  <tr>  
    <td style="border: 1px solid black;">Row 1, Column 1</td>  
    <td style="border: 1px solid black;">Row 1, Column 2</td>  
  </tr>  
</table>  



Additional Considerations  
Content Should Be:  
- Engaging, clear, and informative.  
- Scannable for users by utilizing bullet points, numbered lists, tables, and subheadings.  
- Written with proper grammar and tone consistency.  

If provided text includes conclusions, please exclude them. 
However, if you believe they are very relevant, present them as a summary specifically for this section 
(and under no circumstances should you make them h2 headings). 

Audience Experience:  
Always prioritize user intent. Ask yourself:  
- Is the information easy to digest?  
- Does it provide value to the reader?  

Keyword Usage:  
- Use provided keywords naturally within the text.  
- Do not overuse them; instead, focus on high-quality, conversational language.  

And please - Without ```html and ``` at the beginning and end of the HTML block.  
    """

    return structure_prompt




async def content_summary_prompt():
    content = f"""
    I am writing a long article and have already used a specific block of HTML content. 
    I need you to consider this block when continuing to write and avoid repeating the information unless necessary. 
    Please create a brief summary (in text format) of this block that I can provide in future prompts 
    as a basis for further writing. Output should be in text format and should not exceed 100 words (and do not include 
    any HTML block).
    """
    return content


async def get_combine_info_prompt(general_content, competitors_content):
    full_text = f"""
    Product information: {general_content}
    Competitors' structure: {competitors_content}
    """
    return full_text


async def get_new_content_prompt():
    rewrite_content = \
        f"""
        You will be provided with a JSON and your task is to rewrite the content in a more engaging way.
        Content must be E-E-A-T friendly and you should add something from your own experience or opinion and knowledge.
        Then you need to convert new text into an HTML block, which will then be combined with other HTML blocks. 
        The output must be valid HTML without any PHP or JavaScript code or CSS code (except inline CSS for tables).
        Try to use different keywords (but don t owerspam) and try to make the text more engaging. Try to udnerstend: 
        does this part of content must be big or small, does it need to be more detailed or less detailed (for better
         user experience). Word count may various from 40 to 1000 words.Without ```html and ``` at the beginning and end. 
       """
    return rewrite_content
