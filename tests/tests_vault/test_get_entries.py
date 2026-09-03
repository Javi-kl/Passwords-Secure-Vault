import jwt
from cryptography.fernet import Fernet
from app.core.config import get_settings
from app.core.vault_session_cache import store_vault_session


def test_get_entries_successful(authed_client, db):
    """Con auth -> lista de entradas"""
    (
        authed_client.post(
            "/vault/create", json={"description": "Test", "password": "test_password"}
        ),
    )

    (
        authed_client.post(
            "/vault/create",
            json={"description": "Test2", "password": "test_password1313"},
        ),
    )

    response = authed_client.get("vault/entries")
    assert response.status_code == 200

    entries = response.json()
    assert isinstance(entries, list)
    assert len(entries) == 2
    assert (
        entries[0]["description"] == "Test"
        and entries[0]["password"] == "test_password"
    )
    assert (
        entries[1]["description"] == "Test2"
        and entries[1]["password"] == "test_password1313"
    )


def test_get_entries_without_auth(client):
    """Sin auth -> 401"""
    response = client.get("/vault/entries")
    assert response.status_code == 401


def test_get_entries_empty(authed_client):
    """Usuario sin entradas ve una lista vacia."""
    response = authed_client.get("/vault/entries")
    assert response.status_code == 200
    assert response.json() == []


def test_get_entries_only_mine(authed_client, second_authed_client):
    """Usuario solo ve sus entradas, nunca las de otros usuarios"""

    (
        authed_client.post(
            "/vault/create",
            json={"description": "Netflix", "password": "test_password"},
        ),
    )

    (
        authed_client.post(
            "/vault/create",
            json={"description": "Gmail", "password": "test_password1313"},
        ),
    )

    # Crear segundo usuario,logearse y crear entrada.
    second_authed_client.post(
        "/vault/create", json={"description": "Other Netflix", "password": "otherpass"}
    )

    response = authed_client.get("/vault/entries")
    assert response.status_code == 200
    entries = response.json()
    assert len(entries) == 2
    descriptions = [e["description"] for e in entries]
    assert "Netflix" in descriptions
    assert "Gmail" in descriptions
    assert "Other Netflix" not in descriptions


def test_recover_entries_error_returns_500(authed_client):
    """Entradas cifradas con clave A + sesión con clave B -> 500."""
    authed_client.post(
        "/vault/create",
        json={"description": "Netflix", "password": "test_password"},
    )
    token = authed_client.cookies.get("access_token")
    payload = jwt.decode(
        token, get_settings().SECRET_KEY, algorithms=[get_settings().ALGORITHM]
    )
    vault_session_id = payload["vault_session"]
    store_vault_session(vault_session_id, Fernet(Fernet.generate_key()))

    response = authed_client.get("vault/entries")

    assert response.status_code == 500
    assert response.json()["detail"] == "Error al recuperar la bóveda."
