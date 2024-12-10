from sqlalchemy import Column, Integer, String, Text, BigInteger, func, DateTime

from app.models.base_model import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(BigInteger)
    sender_name = Column(String)
    receiver_id = Column(BigInteger)
    receiver_name = Column(String)
    content = Column(Text)
    voice_file_path = Column(String, nullable=True)
    message_id = Column(BigInteger, index=True, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
