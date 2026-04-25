from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.db.models.user_model import User


class UserRepository:
    @staticmethod
    def create(email: str, password_hash: str, vault_salt: bytes, db: Session) -> User:
        user = User(email=email, password_hash=password_hash, vault_salt=vault_salt)
        db.add(user)
        db.flush()
        return user

    @staticmethod
    def update_password(user_id: int, password_hash: str, db: Session) -> bool:
        update_user_password = (
            update(User).where(User.id == user_id).values(password_hash=password_hash)
        )
        db.execute(update_user_password)
        db.flush()
        return True

    @staticmethod
    def get_by_id(user_id: int, db: Session) -> User | None:
        return db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()

    @staticmethod
    def get_by_email(email: str, db: Session) -> User | None:
        return db.execute(select(User).where(User.email == email)).scalar_one_or_none()
