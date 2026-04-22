import jwt
from cryptography.fernet import Fernet
from fastapi import Depends, HTTPException, Request, status

from app.core.config import get_settings
from app.core.vault_session_cache import get_vault_session as get_cached_session
from app.db.models.user_model import User

from .auth_deps import auth_user

settings = get_settings()


def get_vault_session(request: Request, user: User = Depends(auth_user)) -> Fernet:
    token = request.cookies.get("access_token")
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    vault_session_id = payload.get("vault_session")

    if not vault_session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Vault session not found, please re-login",
        )
    fernet = get_cached_session(vault_session_id)

    if not fernet:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Vault session expired, please re-login",
        )
    return fernet
