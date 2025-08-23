# from functools import lru_cache
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

from app.api.main import api_router
from app.schemas.exceptions import ErrorResponse
from app.settings import settings
from app.utils.exceptions import AppException

logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
    "http://localhost:5173",  # Vite local dev
    "http://127.0.0.1:5173",
    "http://yourdomain.com",  # replace with final domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # origins allowed
    allow_credentials=True,
    allow_methods=["*"],  # allow all HTTP methods
    allow_headers=["*"],  # allow all headers
)


@app.exception_handler(AppException)
async def app_exception_handler(_request: Request, exc: AppException):
    logger.error("AppException: %s | Context: %s", exc.detail, exc.context)
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            detail=exc.detail,
            code=exc.code,
            status_code=exc.status_code,
            context=exc.context,
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_request: Request, exc: Exception):
    logger.exception("Unhandled Exception occurred : %s", exc)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            detail="Internal Server Error", code="internal_error", status_code=500
        ).model_dump(),
    )


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
# add middleware for request and response
# add basic logging setup
