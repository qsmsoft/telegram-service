from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.schemas.userbotinfo import UserBotInfo


class UserBase(BaseModel):
    username: str
    name: str | None = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    userbot_infos: List[UserBotInfo] = []

    class Config:
        from_attributes = True
