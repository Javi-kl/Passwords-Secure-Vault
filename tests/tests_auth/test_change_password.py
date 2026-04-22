from app.repositories.user_repository import UserRepository


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
    old_hash = UserRepository.find_by_email("test@test.com", db).password_hash
    response = authed_client.patch(
        "/auth/password",
        json={
            "current_password": "12345678901234",
            "new_password": "new12345678901234",
            "confirm_password": "new12345678901234",
        },
    )
    assert response.status_code == 200
    new_hash = UserRepository.find_by_email("test@test.com", db).password_hash
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
