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

Product information (“{Product information from Perplexity}”).
Competitors’ structure on the same topic (“{Competitors’ structure on the topic {variable}}”).
Based on these inputs, create a JSON structure that describes an HTML article. The article should:

Be better structured than competitors (avoid overlapping categories, ensure clarity and uniqueness).
Include concise product information in each subcategory.
Where relevant, incorporate tables for structured data presentation.
JSON Structure Guidelines:

H1: The main title, tied to the topic {variable}.
H2: Subcategories (optimized based on competitors’ structure, incorporating product information).
Each subcategory must include:
A brief description summarizing the subcategory and linking it to the product.
H3: Subsections, if necessary. Each subsection may include:
A brief explanation of the subsection’s focus.
Optionally:
A table ([table]) with headers and rows for structured data (e.g., specifications, comparisons).
An image ([Image description]) with a clear description to identify a relevant image.
Video: At the end of the article, include a [Video description] relevant to the product or topic.
Expected Output Format (JSON):
The output must strictly follow this format:

json
Copy code
{
  "title": "Main Title",
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
          },
          "image": "Image description: A relevant image showcasing the subsection."
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
"""
    return html_structure_prompt
