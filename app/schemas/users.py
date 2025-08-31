from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.utils.enums import AuthType, UserRole


class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp_code: str


class UserBase(BaseModel):
    email: EmailStr
    name: str
    is_active: bool = True
    auth_type: AuthType = AuthType.LOCAL
    provider_id: Optional[str] = None
    role: UserRole = UserRole.USER


class UserCreate(UserBase):
    password: Optional[str] = None  # Required for local, ignored for OAuth


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = True
    auth_type: Optional[AuthType] = None
    provider_id: Optional[str] = None
    role: Optional[UserRole] = None


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
