import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import APIKeyHeader

from languages.language_json import *

router = APIRouter(tags=["Languages"])

load_dotenv()

API_KEY = os.getenv("LANGUAGE_API_KEY")
API_KEY_NAME = os.getenv("LANGUAGE_API_NAME")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


def get_api_key(api_key: str = Query(..., description="Your API key")):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key


@router.post("/add_language")
async def add_language(language: str, api_key: str = Depends(get_api_key)):
    return await del_append_language(language, "append")


@router.delete("/delete_language")
async def delete_language(language: str, api_key: str = Depends(get_api_key)):
    return await del_append_language(language, "delete")


@router.get("/show_languages")
async def show_languages():
    return language_json_read()
