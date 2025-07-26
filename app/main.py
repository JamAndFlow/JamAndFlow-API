# from functools import lru_cache
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.sessions import SessionMiddleware

from app.api.main import api_router
from app.settings import settings

app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="JamAndFlow API",
        version="1.0.0",
        description="JamAndFlow API",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# This line adds session middleware to the FastAPI application.
# It allows the application to manage user sessions,
# which is useful for authentication and state management.
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

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
