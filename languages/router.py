import json

from fastapi import APIRouter

from languages.language_json import *

router = APIRouter(tags=["Languages"])


@router.get("/add_language")
async def add_language(language: str):
    return del_append_language(language, "append")


@router.get("/delete_language")
async def delete_language(language: str):
    return del_append_language(language, "delete")


@router.get("/show_languages")
async def show_languages():
    return language_json_read()
