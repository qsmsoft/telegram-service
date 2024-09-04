from datetime import datetime
from typing import List

from pydantic import BaseModel


class UserbotInfoBase(BaseModel):
    api_id: int
    api_hash: str
    phone_number: str


class UserBotInfoCreate(UserbotInfoBase):
    pass


class UserBotInfo(UserbotInfoBase):
    id: int
    organization_id: int


class OrganizationBase(BaseModel):
    name: str
    email: str


class OrganizationCreate(OrganizationBase):
    pass


class Organization(OrganizationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    userbot_infos: List[UserBotInfo] = []

    class Config:
        orm_mode = True
