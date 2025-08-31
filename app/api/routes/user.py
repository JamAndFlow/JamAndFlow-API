from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.users import OTPVerifyRequest, UserCreate, UserResponse
from app.services.user import (
    get_current_user,
    register_with_otp,
    verify_otp_and_create_user,
)

router = APIRouter()


@router.post("/register", status_code=201)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with OTP verification.
    It initiates the OTP process and returns a response to the user.
    The user must then verify the OTP to complete registration."""
    return register_with_otp(db, user_in)


@router.post("/verify-otp", response_model=UserResponse)
def verify_otp(request: OTPVerifyRequest, db: Session = Depends(get_db)):
    """Verify OTP and create user.
    This endpoint is called after the user has received an OTP via email.
    It checks the OTP and creates the user if the OTP is valid."""
    user = verify_otp_and_create_user(db, request.email, request.otp_code)
    return user


@router.get("/me")
def read_users_me(current_user=Depends(get_current_user)):
    if hasattr(current_user, "id"):
        return {
            "id": current_user.id,
            "email": current_user.email,
            "name": current_user.name,
            "role": current_user.role,
            "auth_type": current_user.auth_type,
        }
    return {"user": current_user}
