from app.db.models.vault_model import VaultEntry


def test_update_entry_success(authed_client):
    """Update exitoso -> 200 + mensaje de confirmación."""
    authed_client.post(
        "/vault/create",
        json={"description": "Netflix", "password": "original12345"},
    )
    response = authed_client.patch(
        "/vault/update/1",
        json={"description": "GitHub", "password": "nueva12345"},
    )
    assert response.status_code == 200
    assert "Entrada actualizada." in response.text


def test_update_entry_password_encrypted(authed_client, db):
    """Password actualizado se guarda cifrado, no en texto plano."""
    authed_client.post(
        "/vault/create",
        json={"description": "Netflix", "password": "original12345"},
    )
    authed_client.patch(
        "/vault/update/1",
        json={"description": "GitHub", "password": "nueva12345"},
    )

    entry = db.get(VaultEntry, 1)
    assert entry is not None, "La entrada debería existir tras update."
    assert entry.encrypted_password != "nueva12345"


def test_update_entry_not_found(authed_client, db):
    """Actualizar entrada inexistente -> 404."""
    response = authed_client.patch(
        "/vault/update/9999",
        json={"description": "No existe", "password": "noexiste12345"},
    )
    assert response.status_code == 404


def test_update_entry_other_user_forbidden(authed_client, second_authed_client, db):
    """Usuario no puede actualizar entrada ajena -> 403."""
    authed_client.post(
        "/vault/create",
        json={"description": "Netflix", "password": "netflix12345"},
    )
    entry = db.get(VaultEntry, 1)
    assert entry is not None, "La entrada debería existir tras crearla"
    response = second_authed_client.patch(
        f"/vault/update/{entry.id}",
        json={"description": "Hackeada", "password": "hackeada12345"},
    )
    assert response.status_code == 403


def test_update_entry_data_persisted(authed_client, db):
    """Datos modificados se persisten en BD tras el update."""
    authed_client.post(
        "/vault/create",
        json={"description": "Netflix", "password": "original12345"},
    )
    authed_client.patch(
        "/vault/update/1",
        json={"description": "GitHub", "password": "nueva12345"},
    )
    entry = db.get(VaultEntry, 1)
    assert entry is not None, "La entrada debería existir tras el update"
    assert entry.description == "GitHub"
    assert entry.encrypted_password != "nueva12345"
