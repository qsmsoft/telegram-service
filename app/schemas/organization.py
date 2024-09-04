from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.schemas.schemas import UserBotInfo


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
