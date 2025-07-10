from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import AuthType, User
from app.schemas.users import UserCreate
from app.settings import settings
from app.utils.auth import create_access_token, hash_password, verify_password

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
