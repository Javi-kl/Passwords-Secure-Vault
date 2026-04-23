from pydantic import BaseModel, field_validator


class EntryCreate(BaseModel):
    description: str
    password: str
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return password
