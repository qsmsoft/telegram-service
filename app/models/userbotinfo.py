from sqlalchemy import Column, Integer, String

from app.db.base import Base


class UserbotInfo(Base):
    __tablename__ = "userbot_infos"

    id = Column(Integer, primary_key=True, index=True)
    api_id = Column(Integer, index=True, nullable=False)
    api_hash = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    organization = relationship("Organization", back_populated="userbot_infos")
