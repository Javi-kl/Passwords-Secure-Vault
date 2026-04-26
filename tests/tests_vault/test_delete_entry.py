from app.db.models.vault_model import VaultEntry


def test_delete_entry_success(authed_client, db):
    """Eliminar entrada → 200 + mensaje de confirmación."""
    authed_client.post(
        "/vault/create",
        json={"description": "Netflix", "password": "original12345"},
    )
    response = authed_client.delete(
        "/vault/delete/1",
    )

    assert response.status_code == 200
    assert "Entrada borrada." in response.text


def test_delete_entry_removed_from_db(authed_client, db):
    """Entrada eliminada no existe en BD."""
    authed_client.post(
        "/vault/create",
        json={"description": "Netflix", "password": "netflix12345"},
    )
    authed_client.delete("/vault/delete/1")
    entry = db.get(VaultEntry, 1)
    assert entry is None, "La entrada debería no existir tras eliminarla"


def test_delete_entry_not_found(authed_client, db):
    """Eliminar entrada inexistente → 404."""
    response = authed_client.delete("/vault/delete/9999")
    assert response.status_code == 404


def test_delete_entry_other_user_forbidden(authed_client, second_authed_client, db):
    """Usuario no puede eliminar entrada ajena → 403."""
    authed_client.post(
        "/vault/create",
        json={"description": "Netflix", "password": "netflix12345"},
    )
    entry = db.get(VaultEntry, 1)
    assert entry is not None, "La entrada debería existir tras crearla"
    response = second_authed_client.delete(f"/vault/delete/{entry.id}")
    assert response.status_code == 403
