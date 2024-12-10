from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    api_id = Column(Integer, index=True, unique=True)
    api_hash = Column(String, unique=True)
    phone_number = Column(String, unique=True)
    session_name = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    is_active = Column(Boolean, default=False)
    phone_code_hash = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationship to User
    user = relationship("User", back_populates="telegram_clients")
