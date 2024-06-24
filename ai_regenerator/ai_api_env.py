import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("MY_OPENAI_API_URL")
openai_api_endpoint = os.getenv("MY_OPENAI_API_URL")

openai.api_key = openai_api_key
openai.base_url = openai_api_endpoint

API_endpoint = openai
