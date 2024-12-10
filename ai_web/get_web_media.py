from googleapiclient.discovery import build
from get_env import google_api_key, cx_video, cx_image


def search_youtube_video(query):
    service = build("customsearch", "v1", developerKey=google_api_key)

    res = service.cse().list(
        q=query,
        cx=cx_video,
        num=1
    ).execute()

    if 'items' in res:
        for item in res['items']:
            if 'youtube.com' in item['link']:
                return item['link']
        return "Video not found."
    else:
        return "Video not found."


def search_image(query):
    service = build("customsearch", "v1", developerKey=google_api_key)

    res = service.cse().list(
        q=query,
        cx=cx_image,
        searchType='image',
        num=1,
        imgSize='LARGE'
    ).execute()

    if 'items' in res:
        image_url = res['items'][0]['link']
        return image_url
    else:
        return "Image not found."

