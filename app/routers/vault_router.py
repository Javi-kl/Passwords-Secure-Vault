from typing import Annotated

from cryptography.fernet import Fernet
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models.user_model import User
from app.dependencies.auth_deps import auth_user
from app.dependencies.vault_deps import get_vault_session
from app.schemas.vault_schema import EntryCreate, EntryRead
from app.services.vault_service import VaultService

router = APIRouter(prefix="/vault", tags=["vault"])


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
)
def create_entry(
    entry_data: EntryCreate,
    user: Annotated[User, Depends(auth_user)],
    fernet: Annotated[Fernet, Depends(get_vault_session)],
    db: Annotated[Session, Depends(get_db)],
):
    return VaultService.create_entry(entry_data, user, fernet, db)


@router.get("/entries", status_code=status.HTTP_200_OK, response_model=list[EntryRead])
def get_entries(
    user: Annotated[User, Depends(auth_user)],
    fernet: Annotated[Fernet, Depends(get_vault_session)],
    db: Annotated[Session, Depends(get_db)],
):
    return VaultService.get_entries(user, fernet, db)


@router.patch("/update/{entry_id}", status_code=status.HTTP_200_OK)
def update_entry(
    entry_id: int,
    entry_data: EntryCreate,
    user: Annotated[User, Depends(auth_user)],
    fernet: Annotated[Fernet, Depends(get_vault_session)],
    db: Annotated[Session, Depends(get_db)],
):
    return VaultService.update_entry(entry_id, entry_data, user, fernet, db)


@router.delete("/delete/{entry_id}")
def delete_entry():
    pass
