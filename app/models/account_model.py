from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.base_model import Base, TimestampsMixin

if TYPE_CHECKING:
    from app.models.user_model import User


class Account(Base, TimestampsMixin):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    api_id: Mapped[int] = mapped_column(index=True)
    api_hash: Mapped[str]
    phone_number: Mapped[str]
    session_name: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    is_active: Mapped[bool] = mapped_column(default=False)
    phone_code_hash: Mapped[Optional[str]]

    # Relationship to User
    user: Mapped["User"] = relationship(back_populates="accounts")
