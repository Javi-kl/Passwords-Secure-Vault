import jwt
import secrets

from fastapi.testclient import TestClient
from app.core.config import get_settings

settings = get_settings()


def test_session_not_found_returns_401(client: TestClient):
    resp_register = client.post(
        "/auth/register",
        json={"email": "ana@gmail.com", "password": "UnaClaveSegura2024"},
    )

    payload = {"sub": str(resp_register.json()["id"])}

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    client.cookies.set("access_token", token)
    resp_entries = client.get("/vault/entries")

    assert resp_entries.status_code == 401
    assert "no encontrada" in resp_entries.json()["detail"]


def test_expired_session_returns_401(client: TestClient):
    resp_register = client.post(
        "/auth/register",
        json={"email": "ana@gmail.com", "password": "UnaClaveSegura2024"},
    )
    payload = {
        "sub": str(resp_register.json()["id"]),
        "vault_session": secrets.token_urlsafe(32),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    client.cookies.set("access_token", token)
    resp_entries = client.get("/vault/entries")

    assert resp_entries.status_code == 401
    assert "expirada" in resp_entries.json()["detail"]
