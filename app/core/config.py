from functools import lru_cache

from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    """Configuración de la aplicación cargada desde variables de entorno."""
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    COOKIE_SECURE: bool = True
    VAULT_CACHE_DIR: str
    model_config = ConfigDict(env_file=".env", extra="forbid")

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, value: str) -> str:
        """Rechaza secrets vacíos o menores a 32 chars."""
        if not value or len(value) < 32:
            raise ValueError("SECRET_KEY debe tener al menos 32 caracteres")
        return value


@lru_cache
def get_settings() -> Settings:
    """Singleton de configuración — cacheado tras la primera llamada."""
    return Settings()