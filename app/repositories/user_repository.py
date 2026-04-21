from sqlalchemy.orm import Session

from app.db.models.user_model import User


class UserRepository:
    @staticmethod
    def find_by_email(email: str, db: Session) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create(email: str, password_hash: str, db: Session) -> User:
        user = User(email=email, password_hash=password_hash)
        db.add(user)
        db.flush()
        return user

    @staticmethod
    def find_by_id(user_id: str, db: Session) -> User | None:
        return db.query(User).filter(User.id == user_id).first()
