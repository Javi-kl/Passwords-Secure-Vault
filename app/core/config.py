from functools import lru_cache

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    VAULT_ENCRYPTION_KEY: str
    model_config = ConfigDict(env_file=".env", extra="forbid")


@lru_cache
def get_settings() -> Settings:
    return Settings()
