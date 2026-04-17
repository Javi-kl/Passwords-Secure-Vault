from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import UserCreate, UserResponse


class AuthService:
    @staticmethod
    def register(user_data: UserCreate, db: Session) -> UserResponse:
        existing_user = UserRepository.find_by_email(user_data.email, db)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este email ya está registrado",
            )

        password_hash = hash_password(user_data.password)
        user = UserRepository.create(user_data.email, password_hash, db)
        return UserResponse.model_validate(user)
