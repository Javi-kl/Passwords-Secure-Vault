from functools import lru_cache

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    COOKIE_SECURE: bool = True
    model_config = ConfigDict(env_file=".env", extra="forbid")


@lru_cache
def get_settings() -> Settings:
    return Settings()
