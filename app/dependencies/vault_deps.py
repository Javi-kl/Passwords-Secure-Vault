from typing import Annotated

from cryptography.fernet import Fernet
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.vault_session_cache import get_vault_cached_session
from app.db.database import get_db
from app.db.models.user_model import User
from app.db.models.vault_model import VaultEntry
from app.dependencies.auth_deps import auth_user
from app.repositories.vault_repository import VaultRepository


def get_vault_session(request: Request) -> Fernet:
    vault_session_id = getattr(request.state, "vault_session_id", None)

    if not vault_session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesion de bóveda no encontrada.",
        )
    fernet = get_vault_cached_session(vault_session_id)

    if not fernet:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesion de bóveda expirada.",
        )
    return fernet


def get_owned_entry(
    entry_id: int,
    user: Annotated[User, Depends(auth_user)],
    db: Annotated[Session, Depends(get_db)],
) -> VaultEntry:
    """Valida que la entry exista y pertenezca al usuario autenticado."""

    entry = VaultRepository.get_by_id(entry_id, db)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La entrada no existe.",
        )
    if entry.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a esta entrada.",
        )
    return entry
