from sqlalchemy.orm import Session

from app.db.models.vault_model import VaultEntry


class VaultRepository:
    @staticmethod
    def create_entry(
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
