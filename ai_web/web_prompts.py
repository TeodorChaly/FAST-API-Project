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


def get_html_structure_prompt():
    html_structure_prompt = f"""test"""
    return html_structure_prompt
