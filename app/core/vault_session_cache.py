from cryptography.fernet import Fernet
from diskcache import Cache

from app.core.config import get_settings

settings = get_settings()

TTL_SECONDS = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60

_vault_cache = Cache(settings.VAULT_CACHE_DIR)


def store_vault_session(session_id: str, fernet: Fernet) -> None:
    _vault_cache.set(session_id, fernet, expire=TTL_SECONDS)


def get_vault_cached_session(session_id: str) -> Fernet | None:
    return _vault_cache.get(session_id)


def remove_vault_session(session_id: str) -> None:
    _vault_cache.delete(session_id)
