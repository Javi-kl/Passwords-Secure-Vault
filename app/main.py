from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:8000",
    ],  # Qué dominios pueden llamar a tu API
    allow_credentials=True,  # Permite enviar cookies (tienes cookie httpOnly)
    allow_methods=["*"],  # GET, POST, PUT, DELETE, PATCH, etc.
    allow_headers=["*"],  # Content-Type, Authorization, etc.
)

setup_rate_limiting(app)
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(vault_router)
