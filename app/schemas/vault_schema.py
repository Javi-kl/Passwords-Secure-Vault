from datetime import datetime

from pydantic import BaseModel, field_serializer, field_validator


class EntryCreate(BaseModel):
    description: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return password

    
class EntryRead(BaseModel):
    id: int
    description: str
    password: str
    created_at: datetime
    updated_at: datetime | None = None

    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, dt: datetime, _info):
        if dt is None:
            return None
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    model_config = {"from_attributes": True}
