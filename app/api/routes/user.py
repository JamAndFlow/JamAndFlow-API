
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.users import OTPVerifyRequest, Token, UserCreate, UserResponse
from app.services.user import (get_current_user, login_user, register_with_otp,
                               verify_otp_and_create_user)

router = APIRouter()


@router.post("/register", status_code=201)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    return register_with_otp(db, user_in)


@router.post("/verify-otp", response_model=UserResponse)
def verify_otp(request: OTPVerifyRequest, db: Session = Depends(get_db)):
    user = verify_otp_and_create_user(db, request.email, request.otp_code)
    return user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    return login_user(db, form_data.username, form_data.password)


@router.get("/me", response_model=str)
def read_users_me(current_user=Depends(get_current_user)):
    return current_user
