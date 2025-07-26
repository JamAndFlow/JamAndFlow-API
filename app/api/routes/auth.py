from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.config import Config

from app.settings import settings
from app.utils import auth

router = APIRouter()

# OAuth setup
oauth = OAuth(
    Config(
        environ={
            "GITHUB_CLIENT_ID": settings.GITHUB_CLIENT_ID,
            "GITHUB_CLIENT_SECRET": settings.GITHUB_CLIENT_SECRET,
        }
    )
)
github = oauth.register(
    name="github",
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)


@router.get("/github/login")
def login_via_github(request: Request):
    redirect_uri = request.url_for("auth_github_callback")
    return github.authorize_redirect(request, redirect_uri)


@router.get("/github/callback")
async def auth_github_callback(request: Request):
    try:
        token = await github.authorize_access_token(request)
        resp = await github.get("user", token=token)
        profile = resp.json()
        email = profile.get("email")
        if not email:
            # fetch primary email
            emails_resp = await github.get("user/emails", token=token)
            emails = emails_resp.json()
            primary_email = next(
                (e["email"] for e in emails if e.get("primary") and e.get("verified")),
                None,
            )
            email = primary_email
        if not email:
            raise HTTPException(status_code=400, detail="GitHub email not found")
        # Issue a JWT token for the user
        user_data = {"sub": email, "github_id": profile["id"]}
        jwt_token = auth.create_access_token(user_data)
        return JSONResponse({"access_token": jwt_token, "token_type": "bearer"})
    except OAuthError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
