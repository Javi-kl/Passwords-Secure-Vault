from cryptography.fernet import Fernet
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated
from app.db.database import get_db
from app.db.models.user_model import User
from app.dependencies.vault_deps import get_vault_session
from app.schemas.vault_schema import EntryCreate
from app.services.vault_service import VaultService
from app.dependencies.auth_deps import auth_user

router = APIRouter(prefix="/vault", tags=["vault"])


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
)
def create(
    entry_data: EntryCreate,
    user: Annotated[User, Depends(auth_user)],
    fernet: Annotated[Fernet, Depends(get_vault_session)],
    db: Annotated[Session, Depends(get_db)],
):
    return VaultService.create_entry(entry_data, user, fernet, db)
