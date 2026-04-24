import logging

from cryptography.fernet import Fernet, InvalidToken
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.vault_crypto import decrypt_entry, encrypt_entry
from app.db.models.user_model import User
from app.repositories.vault_repository import VaultRepository
from app.schemas.vault_schema import EntryCreate, EntryRead

logger = logging.getLogger("vault_service")


class VaultService:
    @staticmethod
    def create_entry(entry_data: EntryCreate, user: User, fernet: Fernet, db: Session):
        encrypted_password = encrypt_entry(fernet, entry_data.password)
        VaultRepository.create_entry(
            user.id, entry_data.description, encrypted_password, db
        )
        return {"message": "Entrada creada correctamente"}

    @staticmethod
    def get_entries(user: User, fernet: Fernet, db: Session):
        entries = VaultRepository.find_by_user_id(user.id, db)
        result = []
        try:
            for entry in entries:
                plaintext = decrypt_entry(fernet, entry.encrypted_password)
                result.append(
                    EntryRead(
                        id=entry.id,
                        description=entry.description,
                        password=plaintext,
                        created_at=entry.created_at,
                        updated_at=entry.updated_at,
                    )
                )
            return result
        
        except InvalidToken:
            logger.error("InvalidToken al recuperar entradas del usuario %s", user.id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al recuperar la bóveda.",
            )
        
    @staticmethod
    def re_encrypt_entries(
        old_fernet: Fernet, new_fernet: Fernet, user_id: int, db: Session
    ) -> None:
        entries = VaultRepository.find_by_user_id(user_id, db)
        try:
            for entry in entries:
                plaintext = decrypt_entry(old_fernet, entry.encrypted_password)
                entry.encrypted_password = encrypt_entry(new_fernet, plaintext)

        except InvalidToken:
            logger.error(
                "InvalidToken al re-encriptar entradas del usuario %s", user_id
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar la bóveda.",
            )
