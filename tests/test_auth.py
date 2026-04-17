def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={"email": "ana@gmail.com", "password": "12345678901234"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "ana@gmail.com"
    assert "id" in data
    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_email(client):
    client.post(
        "/auth/register",
        json={"email": "ana@gmail.com", "password": "12345678901234"},
    )
    response = client.post(
        "/auth/register",
        json={"email": "ana@gmail.com", "password": "otracontrasena14"},
    )
    assert response.status_code == 409


def test_register_short_password(client):
    response = client.post(
        "/auth/register",
        json={"email": "ana@gmail.com", "password": "1234567"},
    )
    assert response.status_code == 422


def test_register_invalid_email(client):
    response = client.post(
        "/auth/register",
        json={"email": "no-es-email", "password": "12345678901234"},
    )
    assert response.status_code == 422


def test_register_empty_body(client):
    response = client.post("/auth/register", json={})
    assert response.status_code == 422
