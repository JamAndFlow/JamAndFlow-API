from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.otp import OTP
from app.models.user import AuthType, User
from app.schemas.users import UserCreate
from app.settings import settings
from app.utils.auth import (
    cleanup_expired_otps,
    generate_otp,
    hash_password,
    validate_strong_password,
)
from app.utils.email import send_otp_email

security = HTTPBearer()


def create_user(db: Session, user_in: UserCreate) -> User:
    """Create a new user in the database."""
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = user_in.password if user_in.password else None
    user = User(
        email=user_in.email,
        name=user_in.name,
        password=hashed_password,  # Store hashed password
        is_active=user_in.is_active,
        provider_id=user_in.provider_id,
        auth_type=AuthType(user_in.auth_type.value),
        created_at=datetime.utcnow(),
    )
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Could not create user (integrity error)"
        ) from exc
    return user


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError as exc:
        raise JWTError("JWT validation failed") from exc


def register_with_otp(db: Session, user_in: UserCreate):
    """Register a new user, initiate OTP process, and send OTP to email."""
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    if not user_in.name:
        raise HTTPException(status_code=400, detail="Name is required.")

    validate_strong_password(user_in.password)
    otp_code = generate_otp()

    expires_at = datetime.utcnow() + timedelta(minutes=5)
    hashed_password = hash_password(user_in.password) if user_in.password else None

    otp_entry = OTP(
        email=user_in.email,
        otp_code=otp_code,
        name=user_in.name,
        password=hashed_password,
        is_active=1 if getattr(user_in, "is_active", True) else 0,
        created_at=datetime.utcnow(),
        expires_at=expires_at,
    )
    db.add(otp_entry)
    db.commit()
    send_otp_email(user_in.email, otp_code)
    cleanup_expired_otps(db)
    return {"msg": "OTP sent to email. Please verify to complete registration."}


def verify_otp_and_create_user(db: Session, email: str, otp_code: str):
    otp_entry = (
        db.query(OTP).filter(OTP.email == email, OTP.otp_code == otp_code).first()
    )
    if not otp_entry or otp_entry.is_expired():
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        db.delete(otp_entry)
        db.commit()
        raise HTTPException(status_code=400, detail="User already registered.")

    # Use the existing create_user function with OTP data, in a transaction
    user_in = UserCreate(
        email=otp_entry.email,
        name=otp_entry.name,
        password=otp_entry.password,  # Already hashed
        is_active=bool(otp_entry.is_active),
    )
    try:
        user = create_user(db, user_in)
        db.delete(otp_entry)
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="User creation failed. Please try again."
        ) from exc
    cleanup_expired_otps(db)
    return user
