import logging
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import UserCreate, UserResponse

logger = logging.getLogger("auth_service")
settings = get_settings()


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
    def login(form: OAuth2PasswordRequestForm, db: Session, response: Response):
        user = UserRepository.find_by_email(form.username, db)
        if not user:
            logger.warning("Login fallido para: %s", form.username)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales no válidas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not verify_password(form.password, user.password_hash):
            logger.warning("Login fallido para: %s", form.username)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales no válidas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        payload = {
            "sub": str(user.id),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            max_age=600,
            secure=settings.COOKIE_SECURE,
            samesite="lax",
            path="/",
        )
        logger.info("Login exitoso para: %s", user.email)
        return {"message": "login correcto"}

    @staticmethod
    def logout(response: Response):
        response.delete_cookie(
            key="access_token",
            path="/",
        )
        return {"message": "sesión cerrada"}
