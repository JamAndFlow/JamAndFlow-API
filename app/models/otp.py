
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from app.config.database import Base


class OTP(Base):
    __tablename__ = "otps"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    otp_code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=True)
    is_active = Column(Integer, default=1)  # 1 for True, 0 for False
    provider_id = Column(String, nullable=True)
    auth_type = Column(String, nullable=False, default="local")
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    def is_expired(self):
        return datetime.utcnow() > self.expires_at
