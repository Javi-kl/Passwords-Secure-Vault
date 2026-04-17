from fastapi import FastAPI

from app.db.database import Base, engine
from app.db.models.user_model import User  # noqa: F401
from app.routers.auth_router import router as auth_router

app = FastAPI()

app.include_router(auth_router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)  # cambiar al integrar alembic
