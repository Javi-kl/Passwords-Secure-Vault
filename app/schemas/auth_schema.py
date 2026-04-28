from pydantic import BaseModel, EmailStr, field_validator, model_validator

from app.core.security import validate_password_strength


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:

        return validate_password_strength(password)


class UserResponse(BaseModel):
    id: int
    email: str

    model_config = {"from_attributes": True}


class MessageResponse(BaseModel):
    message: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, new_password: str) -> str:
        return validate_password_strength(new_password)

    @model_validator(mode="after")
    def passwords_match(self) -> "ChangePasswordRequest":
        if self.new_password != self.confirm_password:
            raise ValueError("Las contraseñas no coinciden.")
        return self
