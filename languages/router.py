from fastapi import APIRouter, Depends, dependencies

from configs.prepare_config_file import access_required
from languages.language_json import *

router = APIRouter(tags=["Languages"])


@router.post("/add_language")
async def add_language(language: str, api_key: dependencies = Depends(access_required)):
    return await del_append_language(language, "append")


@router.delete("/delete_language")
async def delete_language(language: str, api_key: dependencies = Depends(access_required)):
    return await del_append_language(language, "delete")


@router.get("/show_languages")
async def show_languages(api_key: dependencies = Depends(access_required)):
    return await language_json_read()
