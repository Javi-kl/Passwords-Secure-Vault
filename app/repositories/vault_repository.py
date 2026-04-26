from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.vault_model import VaultEntry


class VaultRepository:
    @staticmethod
    def create(
        user_id: int, description: str, encrypted_password: str, db: Session
    ) -> VaultEntry:
        entry = VaultEntry(
            user_id=user_id,
            description=description,
            encrypted_password=encrypted_password,
        )
        db.add(entry)
        db.flush()
        return entry

    @staticmethod
    def update(
        entry: VaultEntry, description: str, encrypted_password: str, db: Session
    ) -> bool:
        entry.description = description
        entry.encrypted_password = encrypted_password
        db.flush()
        return True

    @staticmethod
    def delete():
        pass

    @staticmethod
    def get_all_by_user_id(user_id: int, db: Session) -> list[VaultEntry]:
        return list(db.scalars(select(VaultEntry).where(VaultEntry.user_id == user_id)))

    @staticmethod
    def get_by_id(entry_id: int, db: Session) -> VaultEntry | None:
        return db.get(VaultEntry, entry_id)
