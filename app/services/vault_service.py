from fastapi import HTTPException, Response, status
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
from app.db.models.user_model import User
from app.schemas.vault_schema import EntryCreate
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.repositories.vault_repository import VaultRepository
from app.core.vault_crypto import encrypt_entry
class VaultService:
    @staticmethod
    def create_entry(entry_data:EntryCreate, user:User, fernet:Fernet, db:Session):
        encrypted_password = encrypt_entry(fernet,entry_data.password)
        VaultRepository.create_entry(user.id,entry_data.description,encrypted_password,db)
        return {"message": "Entrada creada correctamente"}