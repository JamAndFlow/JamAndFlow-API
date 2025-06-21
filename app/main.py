from fastapi import FastAPI

from app.api.main import api_router

app = FastAPI()


@app.get("/health")
def health_check():
    """
    Health check endpoint to verify that the service is running.
    """
    return {"status": "ok"}


app.include_router(api_router, prefix="/api/v1", tags=["v1"])

# TODO:

# add middleware for CORS
# add middleware for request and response
# add basic logging setup
# add exception handling for common errors
