from dotenv import load_dotenv
from fastapi import APIRouter, Request


load_dotenv()


router = APIRouter(prefix="/auth", tags=["auth"], responses={404: {"description": "Not found"}},)

@router.get("/yandex/login")
async def yandex_login():
    """Redirect user to Yandex login page."""
    pass

@router.get("/yandex/callback")
async def yandex_callback(request: Request):
    """Process the login response from Yandex."""
    pass