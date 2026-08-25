import jwt
import secrets


from datetime import datetime, timedelta, timezone
from app.core.config import get_settings


def test_me_with_valid_cookie(authed_client):
    """usuario autenticado puede acceder a un endpoint protegido."""
    response = authed_client.get("/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@test.com"
    assert "id" in data


def test_me_without_cookie(client):
    """endpoint protegido exige token válido"""
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_me_with_invalid_token(client):
    """token manipulado no pasa la verificación."""
    fake_token = jwt.encode({"sub": "1"}, "clave_falsa", algorithm="HS256")
    client.cookies.set("access_token", fake_token)
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_me_with_expired_token(client, db):
    payload = {
        "sub": "1",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
    }
    settings = get_settings()
    expired_token = jwt.encode(
        payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    client.cookies.set("access_token", expired_token)
    response = client.get("/auth/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales no válidas"


def test_user_not_found_returns_401(client):
    payload = {"sub": "1", "vault_session": secrets.token_urlsafe(32)}
    token = jwt.encode(
        payload, get_settings().SECRET_KEY, algorithm=get_settings().ALGORITHM
    )
    client.cookies.set("access_token", token)
    response = client.get("/auth/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales no válidas"
