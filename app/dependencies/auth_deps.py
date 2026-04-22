import jwt
from fastapi import Depends, HTTPException, Request, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.database import get_db
from app.db.models.user_model import User
from app.repositories.user_repository import UserRepository

settings = get_settings()


def auth_user(request: Request, db: Session = Depends(get_db)) -> User:
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales no válidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = request.cookies.get("access_token")
    if not token:
        raise exception
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise exception
    except InvalidTokenError:
        raise exception

    user = UserRepository.find_by_id(user_id, db)

    if user is None:
        raise exception

    return user


