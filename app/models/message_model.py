import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Text, BigInteger, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sender_id: Mapped[int]
    sender_name: Mapped[str]
    receiver_id: Mapped[int]
    receiver_name: Mapped[str]
    content: Mapped[str]
    voice_file_path: Mapped[Optional[str]]
    message_id: Mapped[Optional[int]] = mapped_column(index=True)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
