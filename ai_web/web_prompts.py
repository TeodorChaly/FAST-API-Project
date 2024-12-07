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
