from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import Token, UserCreate, UserResponse

ACCESS_TOKEN_EXPIRE_MINUTES = get_settings().ACCESS_TOKEN_EXPIRE_MINUTES
SECRET_KEY = get_settings().SECRET_KEY
ALGORITHM = get_settings().ALGORITHM


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

    @staticmethod
    def login(form: OAuth2PasswordRequestForm, db: Session) -> Token:
        user = UserRepository.find_by_email(form.username, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales no válidas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not verify_password(form.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales no válidas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = {
            "sub": user.email,
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        return Token(
            access_token=jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM),
            token_type="bearer",
        )
