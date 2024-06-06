import json

from ai_regenerator.ai_api_env import API_endpoint


def json_loader():
    folder_name = "news_json"
    file_name = f"{folder_name}/crypto.json"
    with open(f"../{file_name}", 'r') as file:
        articles = json.load(file)
    return articles


def ai_generator_function():
    completion = API_endpoint.chat.completions.create(
        model="gpt-3.5-unfiltered",
        messages=[
            {"role": "system",
             "content": "Help me to rewrite the text below in a more SEO way:"},
            {"role": "user", "content": json_loader()[0]["Main Text"]},
        ],
    )

    print(completion.choices[0].message.content)


ai_generator_function()
