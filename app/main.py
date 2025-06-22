# from functools import lru_cache
from fastapi import FastAPI

from app.api.main import api_router
from app.settings import settings

app = FastAPI()

# Uncomment the following lines if you want to use caching for settings
# @lru_cache()
# def get_settings():
#     """
#     Get application settings.
#     This function uses caching to avoid reloading settings on every request.
#     """
#     return settings


@app.get("/health")
def health_check():
    """
    Health check endpoint to verify that the service is running.
    """
    return {"status": "ok"}


app.include_router(api_router, prefix=settings.API_V1_STR, tags=["v1"])

# TODO:

# add middleware for CORS
# add middleware for request and response
# add basic logging setup
# add exception handling for common errors
