from fastapi import APIRouter

router = APIRouter()


@router.get("/about_us", tags=["terms"])
async def other_content():
    return {"other_content": "This is other content"}


@router.get("/contact_us", tags=["terms"])
async def contact_us():
    return {"contact_us": "This is contact us"}


@router.get("/privacy_policy", tags=["terms"])
async def privacy_policy():
    return {"privacy_policy": "This is privacy policy"}


@router.get("/terms_of_use", tags=["terms"])
async def terms_of_service():
    return {"terms_of_service": "This is terms of service"}
