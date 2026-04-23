import time

from cryptography.fernet import Fernet
from app.core.config import get_settings

_vault_cache: dict[str, tuple[Fernet, float]] = {}

settings =get_settings()
TTL_SECONDS = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60 


def store_vault_session(session_id: str, fernet: Fernet) -> None:
    _vault_cache[session_id] = (fernet, time.time())


def get_vault_cached_session(session_id: str) -> Fernet | None:
    entry = _vault_cache.get(session_id)
    if entry is None:
        return None
    fernet, stored_at = entry
    if time.time() - stored_at > TTL_SECONDS:
        del _vault_cache[session_id]
        return None
    return fernet


def remove_vault_session(session_id: str) -> None:
    _vault_cache.pop(session_id, None)
