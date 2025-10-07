from datetime import datetime, timezone

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
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True), nullable=False)

    def is_expired(self):
        return datetime.now(timezone.utc) > self.expires_at
