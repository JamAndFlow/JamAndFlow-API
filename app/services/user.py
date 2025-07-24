from datetime import datetime, timedelta
import random
import re

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import AuthType, User
from app.models.otp import OTP
from app.schemas.users import UserCreate
from app.settings import settings
from app.utils.auth import create_access_token, hash_password, verify_password
from app.utils.email import send_otp_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


def create_user(db: Session, user_in: UserCreate) -> User:
    # Check if user already exists
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_in.password) if user_in.password else None
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
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Could not create user (integrity error)"
        )
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.password:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def login_user(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
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
        # Optionally, fetch user from DB here
        return user_id
    except JWTError:
        raise credentials_exception


def generate_otp():
    return str(random.randint(100000, 999999))


def validate_strong_password(password: str):
    # At least 8 chars, one uppercase, one lowercase, one digit, one special char
    if not password or len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one digit.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one special character.")


def register_with_otp(db: Session, user_in: UserCreate):
    # Check if user already exists
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
        is_active=1 if getattr(user_in, 'is_active', True) else 0,
        provider_id=getattr(user_in, 'provider_id', None),
        auth_type=user_in.auth_type.value if hasattr(user_in, 'auth_type') else 'local',
        created_at=datetime.utcnow(),
        expires_at=expires_at
    )
    db.add(otp_entry)
    db.commit()
    send_otp_email(user_in.email, otp_code)
    cleanup_expired_otps(db)
    return {"msg": "OTP sent to email. Please verify to complete registration."}


def verify_otp_and_create_user(db: Session, email: str, otp_code: str):
    otp_entry = db.query(OTP).filter(OTP.email == email, OTP.otp_code == otp_code).first()
    if not otp_entry or otp_entry.is_expired():
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    # Check if user already exists
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        db.delete(otp_entry)
        db.commit()
        raise HTTPException(status_code=400, detail="User already registered.")
    # Create user from OTP details
    user = User(
        email=otp_entry.email,
        name=otp_entry.name,
        password=otp_entry.password,
        is_active=bool(otp_entry.is_active),
        provider_id=otp_entry.provider_id,
        auth_type=AuthType(otp_entry.auth_type),
        created_at=datetime.utcnow(),
    )
    db.add(user)
    db.delete(otp_entry)
    db.commit()
    db.refresh(user)
    cleanup_expired_otps(db)
    return user


def cleanup_expired_otps(db: Session):
    threshold = datetime.utcnow() - timedelta(minutes=5)
    db.query(OTP).filter(OTP.expires_at < threshold).delete()
    db.commit()
