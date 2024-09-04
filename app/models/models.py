from sqlalchemy import Column, Integer, String, Text, BigInteger, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(BigInteger)
    sender_name = Column(String)
    receiver_id = Column(BigInteger)
    receiver_name = Column(String)
    content = Column(Text)
    voice_file_path = Column(String, nullable=True)


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    userbot_infos = relationship("UserBot", back_populated="organizations")


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
