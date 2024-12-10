from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.base_model import Base

if TYPE_CHECKING:
    from app.models.account_model import Account


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True)
    name: Mapped[Optional[str]]
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relationship to Account
    accounts: Mapped[list["Account"]] = relationship(back_populates="user")
