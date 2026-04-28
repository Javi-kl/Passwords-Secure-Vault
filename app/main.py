from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logging_config import setup_logging
from app.core.rate_limit import setup_rate_limiting
from app.routers.auth_router import router as auth_router
from app.routers.health_router import router as health_router
from app.routers.vault_router import router as vault_router

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    from zxcvbn import zxcvbn

    zxcvbn("warmup")
    yield


app = FastAPI(lifespan=lifespan)

setup_rate_limiting(app)
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(vault_router)
