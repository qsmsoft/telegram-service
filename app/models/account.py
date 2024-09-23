from sqlalchemy import Column, Integer, String, ForeignKey, func, DateTime
from sqlalchemy.orm import relationship

from app.db.session import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    api_id = Column(Integer, index=True, nullable=False)
    api_hash = Column(String, nullable=False)
    phone = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    # Relationship to User
    user = relationship("User", back_populates="accounts")
    # Relationship to Session
    sessions = relationship("Session", back_populates="account")
