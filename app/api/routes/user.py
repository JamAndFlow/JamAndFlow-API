from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.users import Token, UserCreate, UserLogin, UserResponse
from app.services.user import create_user, get_current_user, login_user

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, user_in)
    return user


@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, user_in.email, user_in.password)


@router.get("/me", response_model=str)
def read_users_me(current_user=Depends(get_current_user)):
    return current_user
