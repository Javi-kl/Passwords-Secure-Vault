import jwt
from fastapi import Depends, Request
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.exceptions import unauthorized
from app.db.database import get_db
from app.db.models.user_model import User
from app.repositories.user_repository import UserRepository

settings = get_settings()


def auth_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise unauthorized()
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = int(payload.get("sub", 0))
        request.state.vault_session_id = payload.get("vault_session")

    except (InvalidTokenError, ValueError):
        raise unauthorized()

    user = UserRepository.get_by_id(user_id, db)

    if user is None:
        raise unauthorized()

    return user
