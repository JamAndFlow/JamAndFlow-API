from fastapi import APIRouter, Depends

from app.rbac import check_for_permission
from app.settings import settings
from app.utils.http_client import make_request

router = APIRouter()


GENERATOR_SERVICE_URL = settings.GENERATOR_SERVICE_URL


@router.get("/daily_questions")
def get_daily_questions(
    _check_permission=Depends(check_for_permission("VIEW_QUESTIONS")),
):
    """Fetch daily questions from the external generator service."""
    url = f"{GENERATOR_SERVICE_URL}/api/v1/questions/get_daily_question"
    return make_request("GET", url)
