from datetime import datetime

from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.config import Config

from app.config.database import get_db
from app.models.user import AuthType, User
from app.settings import settings
from app.utils import auth

router = APIRouter()

# TODO: Move this to a separate config file
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
async def login_via_github(request: Request):
    """Initiates the GitHub OAuth login flow."""
    redirect_uri = request.url_for("auth_github_callback")
    return await github.authorize_redirect(request, redirect_uri)


@router.get("/github/callback")
async def auth_github_callback(request: Request, db: Session = Depends(get_db)):
    """Handles the GitHub OAuth callback and logs in or registers the user."""
    try:
        token = await github.authorize_access_token(request)
        resp = await github.get("user", token=token)
        profile = resp.json()
        email = profile.get("email")
        name = profile.get("name") or profile.get("login")
        provider_id = str(profile.get("id"))

        # If email is not public, fetch from emails endpoint
        if not email:
            emails_resp = await github.get("user/emails", token=token)
            emails = emails_resp.json()
            email = next(
                (e["email"] for e in emails if e.get("primary") and e.get("verified")),
                None,
            )
            if not email:
                raise HTTPException(
                    status_code=400, detail="GitHub account has no accessible email."
                )

        user = db.query(User).filter(User.email == email).first()
        if not user:
            # TODO: Use existing create user logic
            user = User(
                email=email,
                name=name,
                provider_id=provider_id,
                auth_type=AuthType.GITHUB,
                is_active=True,
                created_at=datetime.utcnow(),
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        access_token = auth.create_access_token(
            {"sub": str(user.id), "email": user.email}
        )
        return JSONResponse({"access_token": access_token, "token_type": "bearer"})
    except OAuthError as e:
        # Log the detailed exception for debugging purposes
        import logging
        logging.error("OAuthError occurred during GitHub authentication", exc_info=e)
        # Return a generic error message to the client
        return JSONResponse({"error": "An error occurred during authentication. Please try again later."}, status_code=400)
