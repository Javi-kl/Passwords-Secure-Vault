from cryptography.fernet import Fernet
from fastapi import Depends, HTTPException, Request, status

from app.core.vault_session_cache import get_vault_cached_session
from app.db.models.user_model import User

from .auth_deps import auth_user


def get_vault_session(request: Request, user: User = Depends(auth_user)) -> Fernet:
    vault_session_id = getattr(request.state, "vault_session_id", None)

    if not vault_session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Vault session not found, please re-login",
        )
    fernet = get_vault_cached_session(vault_session_id)

    if not fernet:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Vault session expired, please re-login",
        )
    return fernet
