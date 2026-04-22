from pydantic import BaseModel, EmailStr, field_validator, model_validator


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if len(password) < 14:
            raise ValueError("La contraseña debe tener al menos 14 caracteres")
        return password


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
        if len(new_password) < 14:
            raise ValueError("La contraseña debe tener al menos 14 caracteres")
        return new_password

    @model_validator(mode="after")
    def passwords_match(self) -> "ChangePasswordRequest":
        if self.new_password != self.confirm_password:
            raise ValueError("Las contraseñas no coinciden.")
        return self
