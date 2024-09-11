from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.schemas.account import AccountRead


class UserBase(BaseModel):
    username: str
    name: str | None = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    accounts: List[AccountRead] = []

    class Config:
        from_attributes = True
