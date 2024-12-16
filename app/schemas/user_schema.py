from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.account_schema import AccountResponse


class UserBase(BaseModel):
    username: str
    name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    accounts: List[AccountResponse]

    class Config:
        from_attributes = True


class UserFilter(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    created_at_start: Optional[str] = None
    created_at_end: Optional[str] = None

