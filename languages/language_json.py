import json

from content.news_file_extractor import language_to_code


async def language_json_read():
    with open("languages/languages.json", "r", encoding="utf-8") as file:
        languages_list = json.load(file)
    return languages_list


async def languages_to_code():
    languages = await language_json_read()
    decoded_languages = []
    for i in languages:
        decoded_languages.append(language_to_code(i))
    return decoded_languages


async def del_append_language(language, action):
    languages_list = await language_json_read()
    if action == "append":
        if language not in languages_list:
            try:
                if language_to_code(language) is not None:
                    languages_list.append(language)

                    with open("languages/languages.json", "w", encoding="utf-8") as file:
                        json.dump(languages_list, file, indent=4)
                    return f"{language} language was added."
                else:
                    return f"Langauge was not added. Error during given language converting."
            except Exception as e:
                return f"Langauge was not added. Error during given language converting."

        else:
            return f"{language} language already exist."

    elif action == "delete":
        if language in languages_list:
            languages_list.remove(language)
            with open("languages/languages.json", "w", encoding="utf-8") as file:
                json.dump(languages_list, file, indent=4)
            return f"{language} language deleted."
        else:
            return f"{language} language was not found."
