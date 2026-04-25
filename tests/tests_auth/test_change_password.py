from app.core.vault_crypto import create_fernet, decrypt_entry
from app.db.models.vault_model import VaultEntry
from app.repositories.user_repository import UserRepository


def test_change_password_reencrypt_entries(authed_client, db):
    """Cambiar contraseña re-encripta las entradas y siguen siendo legibles"""
    # 1 ─ Crear una entrada en la bóveda vía API
    response = authed_client.post(
        "/vault/create", json={"description": "Mi secreto", "password": "secreto12345"}
    )
    assert response.status_code == 201

    # 2 ─ Capturar el ciphertext ORIGINAL antes del cambio de contraseña
    old_entry = db.query(VaultEntry).filter(VaultEntry.user_id == 1).first()
    old_ciphertext = old_entry.encrypted_password

    # 3 ─ Cambiar la contraseña
    response = authed_client.patch(
        "/auth/password",
        json={
            "current_password": "12345678901234",
            "new_password": "newpassword123456",
            "confirm_password": "newpassword123456",
        },
    )
    assert response.status_code == 200

    # 4 ─ Verificar que el ciphertext cambió (re-encriptación real, no el mismo)
    db.refresh(old_entry)
    assert old_entry.encrypted_password != old_ciphertext

    # 5 ─ Verificar que se puede descifrar con la NUEVA contraseña
    user = UserRepository.get_by_email("test@test.com", db)
    new_fernet = create_fernet("newpassword123456", user.vault_salt)
    plaintext = decrypt_entry(new_fernet, old_entry.encrypted_password)
    assert plaintext == "secreto12345"


def test_change_password_empty_vault(authed_client, db):
    """Cambiar contraseña sin entradas en la bóveda funciona correctamente"""
    assert db.query(VaultEntry).count() == 0

    response = authed_client.patch(
        "/auth/password",
        json={
            "current_password": "12345678901234",
            "new_password": "newpassword123456",
            "confirm_password": "newpassword123456",
        },
    )
    assert response.status_code == 200
    assert db.query(VaultEntry).count() == 0


def test_change_password_keeps_entries_unchanged_on_failure(db, client):
    """Si el cambio falla (contraseña actual incorrecta), las entradas no cambian"""
    # 1 ─ Registrar usuario y crear entrada vía API
    client.post(
        "/auth/register", json={"email": "test@test.com", "password": "12345678901234"}
    )
    client.post(
        "/auth/login", data={"username": "test@test.com", "password": "12345678901234"}
    )
    client.post(
        "/vault/create", json={"description": "Mi secreto", "password": "secreto12345"}
    )

    # 2 ─ Capturar el ciphertext original
    old_entry = db.query(VaultEntry).first()
    original_ciphertext = old_entry.encrypted_password

    # 3 ─ Intentar cambiar la contraseña con una incorrecta
    response = client.patch(
        "/auth/password",
        json={
            "current_password": "wrongpassword1",
            "new_password": "newpassword123456",
            "confirm_password": "newpassword123456",
        },
    )

    assert response.status_code == 401

    # 4 ─ Verificar que la entrada NO cambió
    db.refresh(old_entry)
    assert old_entry.encrypted_password == original_ciphertext


def test_change_password_unauthenticated(client):
    """Sin cookie/token → 401 Unauthorized"""
    response = client.patch(
        "/auth/password",
        json={
            "current_password": "12345678901234",
            "new_password": "newpassword123456",
            "confirm_password": "newpassword123456",
        },
    )
    assert response.status_code == 401


def test_change_password_valid(authed_client, db):
    """Datos válidos actualizan la contraseña y devuelven 200"""
    old_hash = UserRepository.get_by_email("test@test.com", db).password_hash
    response = authed_client.patch(
        "/auth/password",
        json={
            "current_password": "12345678901234",
            "new_password": "new12345678901234",
            "confirm_password": "new12345678901234",
        },
    )
    assert response.status_code == 200
    new_hash = UserRepository.get_by_email("test@test.com", db).password_hash
    assert old_hash != new_hash


def test_change_password_mismatch(authed_client):
    """Contraseñas nuevas que no coinciden devuelven 422"""
    response = authed_client.patch(
        "/auth/password",
        json={
            "current_password": "12345678901234",
            "new_password": "newpassword123456",
            "confirm_password": "different1234567",
        },
    )
    assert response.status_code == 422


def test_change_password_wrong_current(authed_client):
    """Contraseña actual incorrecta devuelve 401"""
    response = authed_client.patch(
        "/auth/password",
        json={
            "current_password": "wrongpassword1",
            "new_password": "newpassword123456",
            "confirm_password": "newpassword123456",
        },
    )
    assert response.status_code == 401


def test_change_password_same_as_current(authed_client):
    """Nueva contraseña igual a la actual devuelve 400"""
    response = authed_client.patch(
        "/auth/password",
        json={
            "current_password": "12345678901234",
            "new_password": "12345678901234",
            "confirm_password": "12345678901234",
        },
    )
    assert response.status_code == 400
