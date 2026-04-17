import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose.exceptions import JWTError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.database import get_db
from app.db.models.user_model import User
from app.repositories.user_repository import UserRepository

SECRET_KEY = get_settings().SECRET_KEY
ALGORITHM = get_settings().ALGORITHM

oauth2 = OAuth2PasswordBearer(tokenUrl="auth/login")


def auth_user(
    token: str = Depends(oauth2), db: Session = Depends(get_db)
) -> User | None:
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales no válidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        email = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if email is None:
            raise exception
    except JWTError:
        raise exception

    return UserRepository.find_by_email(email, db)
