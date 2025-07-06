from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.users import UserCreate, UserResponse
from app.services.user import create_user

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=201)
def create_user_endpoint(user_in: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, user_in)
    return user
