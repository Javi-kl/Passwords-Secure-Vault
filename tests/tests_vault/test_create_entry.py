from app.core.vault_crypto import create_fernet, decrypt_entry
from app.db.models.user_model import User
from app.db.models.vault_model import VaultEntry
from app.repositories.user_repository import UserRepository
from app.repositories.vault_repository import VaultRepository


def test_create_entry_success(authed_client, db):
    """Crear entrada -> 201 + entrada en BD."""
    response = authed_client.post(
        "/vault/create",
        json={"description": "Mi secreto", "password": "secreto12345"},
    )
    user = UserRepository.get_by_email("test@test.com", db)
    assert user is not None, "El usuario debería existir (authed_client lo creó)"
    entries = VaultRepository.get_all_by_user_id(user.id, db)

    assert len(entries) == 1
    assert response.status_code == 201
    assert "Entrada creada correctamente" in response.text


def test_create_entry_password_encrypted(authed_client, db):
    """Password se guarda cifrado, no en texto plano."""
    response = authed_client.post(
        "/vault/create",
        json={"description": "GitHub", "password": "gh_pass_12345"},
    )
    entry = (
        db.query(VaultEntry)
        .filter(VaultEntry.description == "GitHub", VaultEntry.user_id == 1)
        .first()
    )
    assert entry is not None
    assert entry.encrypted_password != "gh_pass_12345"


def test_create_entry_decrypt_roundtrip(authed_client, db):
    """Cifrar + descifrar recupera la entrada original."""
    response = authed_client.post(
        "/vault/create",
        json={"description": "GitHub", "password": "gh_pass_12345"},
    )
    user = UserRepository.get_by_email("test@test.com", db)
    assert user is not None, "El usuario debería existir (authed_client lo creó)"
    entry = VaultRepository.get_all_by_user_id(user.id, db)[0]

    user_obj = db.query(User).filter(User.id == user.id).first()

    fernet_key = create_fernet("12345678901234", user_obj.vault_salt)
    plaintext = decrypt_entry(fernet_key, entry.encrypted_password)

    assert plaintext == "gh_pass_12345"


def test_create_entry_unauthenticated(client):
    """Sin autenticación -> 401"""
    response = client.post(
        "/vault/create",
        json={"description": "Test", "password": "test_password"},
    )
    assert response.status_code == 401


def test_create_entry_short_password(authed_client):
    response = authed_client.post(
        "/vault/create",
        json={"description": "Test", "password": "test"},
    )
    assert response.status_code == 422
