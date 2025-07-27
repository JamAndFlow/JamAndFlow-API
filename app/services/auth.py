import logging

from authlib.integrations.starlette_client import OAuthError
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.config.github import github
from app.models.user import User
from app.schemas.users import AuthType, UserCreate
from app.services.user import create_user
from app.utils.auth import create_access_token, verify_password


def authenticate_user(db, email: str, password: str):
    """Authenticate user with email and password using hashed password."""
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.password:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def login_user(db, email: str, password: str):
    """Login user with email and password. Returns an access token if successful. Raises HTTPException if authentication fails."""
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


def create_github_user(profile, email: str, db):
    """Create a new user from GitHub profile data."""
    name = profile.get("name") or profile.get("login")
    provider_id = str(profile.get("id"))

    user_in = UserCreate(
        email=email,
        name=name,
        is_active=True,
        provider_id=provider_id,
        auth_type=AuthType.github,
    )
    user = create_user(db, user_in)
    return user


async def login_github_user(request, db):
    """Login user via GitHub OAuth. Returns an access token if successful. Raises HTTPException if authentication fails."""
    try:
        token = await github.authorize_access_token(request)
        resp = await github.get("user", token=token)
        profile = resp.json()
        email = profile.get("email")

        # If email is not public, fetch from emails endpoint
        if not email:
            emails_resp = await github.get("user/emails", token=token)
            emails = emails_resp.json()
            email = next(
                (
                    e.get("email")
                    for e in emails
                    if e.get("primary") and e.get("verified")
                ),
                None,
            )
            if not email:
                raise HTTPException(
                    status_code=400, detail="GitHub account has no accessible email."
                )

        user = db.query(User).filter(User.email == email).first()

        # If user does not exist, create a new one
        if not user:
            user = create_github_user(profile, email, db)

        access_token = create_access_token({"sub": str(user.id), "email": user.email})
        return JSONResponse({"access_token": access_token, "token_type": "bearer"})
    except OAuthError as e:
        logging.error("OAuthError occurred during GitHub authentication", exc_info=e)
        return JSONResponse(
            {
                "error": "An error occurred during authentication. Please try again later."
            },
            status_code=400,
        )
