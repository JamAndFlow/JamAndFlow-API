from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.github import github
from app.config.google import google
from app.schemas.users import Token
from app.services.auth import login_github_user, login_google_user, login_user

router = APIRouter()


# Standard username/password login route
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """Simple login route using username and password."""
    return login_user(db, form_data.username, form_data.password)


@router.get("/github/login")
async def login_via_github(request: Request):
    """Initiates the GitHub OAuth login flow."""
    redirect_uri = request.url_for("auth_github_callback")
    return await github.authorize_redirect(request, redirect_uri)


# Google OAuth login route
@router.get("/google/login")
async def login_via_google(request: Request):
    """Initiates the Google OAuth login flow."""
    redirect_uri = request.url_for("auth_google_callback")
    return await google.authorize_redirect(request, redirect_uri)


@router.get("/github/callback")
async def auth_github_callback(request: Request, db: Session = Depends(get_db)):
    """Handles the GitHub OAuth callback and logs in or registers the user."""
    return await login_github_user(request, db)


# Google OAuth callback route
@router.get("/google/callback")
async def auth_google_callback(request: Request, db: Session = Depends(get_db)):
    """Handles the Google OAuth callback and logs in or registers the user."""
    return await login_google_user(request, db)
