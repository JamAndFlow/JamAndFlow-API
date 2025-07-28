from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from app.settings import settings

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
