from fastapi import APIRouter, Depends

from app.rbac import check_for_permission
from app.schemas.questions import TechDescription
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

#TODO: user prompt should be in request body
@router.post("/generate_question")
def generate_question(
    user_prompt: str,
    _check_permission=Depends(check_for_permission("VIEW_QUESTIONS")),
):
    """Generate a new question based on topic and difficulty."""
    #TODO: change endpoint to generate_question
    url = f"{GENERATOR_SERVICE_URL}/api/v1/questions/generate_daily_question"

    payload = {"user_prompt": user_prompt}
    return make_request("POST", url, json=payload)


@router.post("/add_tech_description")
def add_tech_description(
    request: TechDescription,
    _check_permission=Depends(check_for_permission("VIEW_QUESTIONS")),
):
    """Add a technical description to a question."""
    url = f"{GENERATOR_SERVICE_URL}/api/v1/questions/add_tech_description"
    payload = request.model_dump()
    return make_request("POST", url, json=payload)
