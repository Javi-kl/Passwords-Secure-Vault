from datetime import datetime, timedelta, timezone

import jwt


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
    fake_token = jwt.encode({"sub": "test@test.com"}, "clave_falsa", algorithm="HS256")
    client.cookies.set("access_token", fake_token)
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_me_with_expired_token(client, db):
    """token expirado devuelve 401"""
    from app.core.config import get_settings
    from app.core.security import hash_password
    from app.repositories.user_repository import UserRepository

    UserRepository.create("test@test.com", hash_password("12345678901234"), db)
    db.commit()
    
    payload = {
        "sub": "test@test.com",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
    }
    settings = get_settings()
    expired_token = jwt.encode(
        payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    client.cookies.set("access_token", expired_token)
    response = client.get("/auth/me")
    assert response.status_code == 401
