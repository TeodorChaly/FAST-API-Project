import json


def language_json_read():
    with open("languages/languages.json", "r", encoding="utf-8") as file:
        languages_list = json.load(file)
    return languages_list


def del_append_language(language, action):
    languages_list = language_json_read()

    if action == "append":
        if language not in languages_list:
            languages_list.append(language)

            with open("languages/languages.json", "w", encoding="utf-8") as file:
                json.dump(languages_list, file, indent=4)
            return f"{language} language was added."
        else:
            return f"{language} language already exist."
    elif action == "delete":
        if language in languages_list:
            languages_list.remove(language)
            with open("languages/languages.json", "w", encoding="utf-8") as file:
                json.dump(languages_list, file, indent=4)
            return f"{language} language deleted."
        else:
            return f"{language} language found."
