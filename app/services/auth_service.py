import logging
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from cryptography.fernet import InvalidToken
from fastapi import HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import hash_password, verify_password
from app.core.vault_crypto import create_fernet, generate_vault_salt, re_encrypt
from app.core.vault_session_cache import remove_vault_session, store_vault_session
from app.db.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.repositories.vault_repository import VaultRepository
from app.schemas.auth_schema import ChangePasswordRequest, UserCreate, UserResponse

logger = logging.getLogger("auth_service")
settings = get_settings()


class AuthService:
    @staticmethod
    def register(user_data: UserCreate, db: Session) -> UserResponse:
        existing_user = UserRepository.get_by_email(user_data.email, db)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este email ya está registrado",
            )
        vault_salt = generate_vault_salt()
        password_hash = hash_password(user_data.password)
        user = UserRepository.create(user_data.email, password_hash, vault_salt, db)
        return UserResponse.model_validate(user)

    @staticmethod
    def login(form: OAuth2PasswordRequestForm, db: Session, response: Response):
        user = UserRepository.get_by_email(form.username, db)
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
        fernet = create_fernet(form.password, user.vault_salt)
        vault_session_id = secrets.token_urlsafe(32)
        store_vault_session(vault_session_id, fernet)

        payload = {
            "sub": str(user.id),
            "vault_session": vault_session_id,
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            secure=settings.COOKIE_SECURE,
            samesite="lax",
            path="/",
        )
        logger.info("Login exitoso para: %s", user.email)
        return {"message": "login correcto"}

    @staticmethod
    def change_password(
        user: User,
        password_data: ChangePasswordRequest,
        db: Session,
        vault_session_id: str | None,
    ):
        if not verify_password(password_data.current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales no válidas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if password_data.current_password == password_data.new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La nueva contraseña no puede ser igual a la actual.",
            )
        old_fernet = create_fernet(password_data.current_password, user.vault_salt)
        new_fernet = create_fernet(password_data.new_password, user.vault_salt)

        entries = VaultRepository.get_all_by_user_id(user.id, db)

        try:
            for entry in entries:
                entry.encrypted_password = re_encrypt(
                    entry.encrypted_password, old_fernet, new_fernet
                )
        except InvalidToken:
            logger.error(
                "InvalidToken al re-encriptar entradas del usuario %s", user.id
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar la bóveda.",
            )
        
        UserRepository.update_password(
            user, hash_password(password_data.new_password), db
        )

        if vault_session_id:
            store_vault_session(vault_session_id, new_fernet)

        return {"message": "Contraseña actualizada correctamente"}

    @staticmethod
    def logout(response: Response, request: Request, vault_session_id: str | None):

        if vault_session_id:
            remove_vault_session(vault_session_id)
        response.delete_cookie(
            key="access_token",
            path="/",
        )

        return {"message": "sesión cerrada"}
