import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.base_model import Base

if TYPE_CHECKING:
    from app.models.user_model import User


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    api_id: Mapped[int] = mapped_column(index=True)
    api_hash: Mapped[str]
    phone_number: Mapped[str]
    session_name: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    is_active: Mapped[bool] = mapped_column(default=False)
    phone_code_hash: Mapped[Optional[str]]
    created_by: Mapped[Optional[int]]
    updated_by: Mapped[Optional[int]]
    deleted_by: Mapped[Optional[int]]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    deleted_at: Mapped[Optional[datetime.datetime]]

    # Relationship to User
    user: Mapped["User"] = relationship(back_populates="accounts")
