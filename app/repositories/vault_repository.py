from sqlalchemy import update
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
        entry_id: int, description: str, encrypted_password: str, db: Session
    ) -> bool:
        update_entry = (
            update(VaultEntry)
            .where(VaultEntry.id == entry_id)
            .values(description=description, encrypted_password=encrypted_password)
        )
        db.execute(update_entry)
        db.flush()
        return True

    @staticmethod
    def delete() -> bool:
        pass

    @staticmethod
    def get_all_by_user_id(user_id: int, db: Session) -> list[VaultEntry]:
        return db.query(VaultEntry).filter(VaultEntry.user_id == user_id).all()

    @staticmethod
    def get_by_id(entry_id: int, db: Session) -> VaultEntry | None:
        return db.query(VaultEntry).filter(VaultEntry.id == entry_id).first()
