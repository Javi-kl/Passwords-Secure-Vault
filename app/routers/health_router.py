from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db

router = APIRouter(tags=["health"])


@router.get("/health", status_code=status.HTTP_200_OK)
def health_check(db: Session = Depends(get_db)):
    """Verifica que la app y la BD están operativas.
    ejecuta una query ligera (SELECT 1) para confirmar la conexión.
    """
    db.execute(text("SELECT 1"))
    return {"status": "ok"}
