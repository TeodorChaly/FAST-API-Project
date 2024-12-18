from dotenv import load_dotenv
import os

load_dotenv()

perplexity = os.getenv("PERPLEXITY_API_KEY")
google_api_key = os.getenv("GOOGLE_API")
cx_image = os.getenv("GOOGLE_IMAGE")
cx_video = os.getenv("YOUTUBE_VIDEO")
xml_river_key = os.getenv("XML_RIVER")
xml_river_user = os.getenv("XML_RIVER_USER")
