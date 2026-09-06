import os

from dotenv import load_dotenv
from fastapi import APIRouter, Request

from fastapi_sso.sso.yandex import YandexSSO


load_dotenv()

yandex_sso = YandexSSO(
    client_id=os.environ["YANDEX_CLIENT_ID"],
    client_secret=os.environ["YANDEX_CLIENT_SECRET"],
    redirect_uri=os.environ["YANDEX_REDIRECT_URL"],
)

router = APIRouter(prefix="/auth", tags=["auth"], responses={404: {"description": "Not found"}},)

@router.get("/yandex/login")
async def yandex_login():
    """Redirect user to Yandex login page."""
    async with yandex_sso:
        return await yandex_sso.get_login_redirect()


@router.get("/yandex/callback")
async def yandex_callback(request: Request):
    """Process the login response from Yandex."""
    print(request.cookies)
    async with yandex_sso:
        user = await yandex_sso.verify_and_process(request)
        print(user)
        if not user:
            return {"error": "Failed to login with Yandex"}

        # Here you can create or log the user into your database
        return {
            "message": "Successfully authenticated!",
            "email": user.email,
            "name": user.display_name,
            "id": user.id,
    }
