from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer, String

from app.config.database import Base
from app.utils.enums import AuthType, UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=True)  # Only for local auth
    is_active = Column(Boolean, default=True)
    provider_id = Column(
        String, unique=True, nullable=True
    )  # For OAuth or external providers
    auth_type = Column(SQLEnum(AuthType), nullable=False, default=AuthType.LOCAL)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.USER)
    created_at = Column(DateTime, nullable=False)
