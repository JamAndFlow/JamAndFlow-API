from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import AuthType, User
from app.schemas.users import UserCreate


def create_user(db: Session, user_in: UserCreate) -> User:
    # Check if user already exists
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=user_in.email,
        name=user_in.name,
        password=user_in.password,  # In production, hash the password!
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
