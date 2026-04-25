from cryptography.fernet import Fernet
from fastapi import HTTPException, Request, status

from app.core.vault_session_cache import get_vault_cached_session


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
