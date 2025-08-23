from fastapi import APIRouter

from app.api.routes import auth, questions, user

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(questions.router, prefix="/questions", tags=["questions"])
