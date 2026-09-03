import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import get_db, ping

logger = logging.getLogger("health")
router = APIRouter(tags=["health"])


@router.get("/health", status_code=status.HTTP_200_OK)
def health_check(db: Annotated[Session, Depends(get_db)]):
    try:
        ping(db)
    except SQLAlchemyError:
        logger.warning("Health check: BD no disponible")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Base de datos no disponible",
        )

    return {"status": "ok"}
