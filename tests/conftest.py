import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings
from app.db.database import Base, get_db
from app.main import app

settings = get_settings()
test_engine = create_engine(settings.TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(bind=test_engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def reset_limiter():
    app.state.limiter.reset()
    yield

@pytest.fixture
def authed_client(client):
    """Cliente con cookie de autenticación seteada."""
    client.post("/auth/register", json={"email": "test@test.com", "password": "12345678901234"})
    client.post("/auth/login", data={"username": "test@test.com", "password": "12345678901234"})
    return client
    
