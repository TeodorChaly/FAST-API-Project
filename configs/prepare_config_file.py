import os
from fastapi import HTTPException
from datetime import datetime
from starlette import status


def create_config_file():
    config_dir = "configs"
    config_file_path = os.path.join(config_dir, "config_setup.py")

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    if not os.path.exists(config_file_path):
        with open(config_file_path, 'w', encoding="utf-8") as config_file:
            config_file.write('''\
# Run background function
dict_of_tasks = [""]  # Name of category to run in background. For example 'news'

# Main site
main_site_topic = ""  # Main site category. For example 'news'

SITE_DOMAIN = ""  # Site domain. For example 'https://example.com' (Don't add '/' at the end!!!)
SITE_NAME = ""  # Site name. For example 'Example'

main_language = ""  # Main language. For example 'en'

google_id_tag = ""  # Google ID tag. Leave empty if you don't have one
''')


active_sessions = {}


def check_access():
    expiry_time = active_sessions.get("user")
    if expiry_time is None or datetime.utcnow() > expiry_time:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access expired or not granted")


async def access_required():
    check_access()
