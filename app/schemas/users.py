from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr


class AuthType(str, Enum):
    local = "local"
    google = "google"
    github = "github"
    # Add more as needed


class UserBase(BaseModel):
    email: EmailStr
    name: str
    is_active: bool = True
    auth_type: AuthType = AuthType.local
    provider_id: Optional[str] = None


class UserCreate(UserBase):
    password: Optional[str] = None  # Required for local, ignored for OAuth


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = True
    auth_type: Optional[AuthType] = None
    provider_id: Optional[str] = None


class UserInDB(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
