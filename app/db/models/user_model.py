from datetime import datetime, timezone

from sqlalchemy import DateTime, String,LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List
from app.db.database import Base

if TYPE_CHECKING:
    from .vault_model import VaultEntry
    
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    vault_salt: Mapped[bytes] = mapped_column(LargeBinary(16),nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    vault_entries: Mapped[List["VaultEntry"]] = relationship(
        "VaultEntry",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )