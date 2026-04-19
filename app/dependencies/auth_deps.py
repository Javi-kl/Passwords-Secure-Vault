import jwt
from fastapi import Depends, HTTPException, Request, status
from jose.exceptions import JWTError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.database import get_db
from app.db.models.user_model import User
from app.repositories.user_repository import UserRepository

SECRET_KEY = get_settings().SECRET_KEY
ALGORITHM = get_settings().ALGORITHM


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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise exception
    except JWTError:
        raise exception

    user = UserRepository.find_by_email(email, db)

    if user is None:
        raise exception

    return user
