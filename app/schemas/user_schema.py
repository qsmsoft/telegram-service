from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.account_schema import AccountResponse


class UserBase(BaseModel):
    username: str
    name: Optional[str] = None

    class Config:
        from_attributes = True


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

    @classmethod
    def from_orm(cls, obj):
        return cls(
            accounts=[AccountResponse(id=account.id, api_id=account.api_id, api_hash=account.api_hash,
                                      phone_number=account.phone_number, user_id=account.user_id,
                                      is_active=account.is_active) for account in obj.accounts]
        )


class UserFilter(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    created_at_start: Optional[datetime] = None
    created_at_end: Optional[datetime] = None
