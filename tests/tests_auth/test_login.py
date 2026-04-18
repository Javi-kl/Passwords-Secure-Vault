def test_login_success(client):
    # crea usuario
    client.post(
        "/auth/register",
        json={"email": "ana@gmail.com", "password": "12345678901234"},
    )
    # Login con form-data
    response = client.post(
        "/auth/login",
        data={"username": "ana@gmail.com", "password": "12345678901234"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_email(client):
    client.post(
        "/auth/register",
        json={"email": "ana@gmail.com", "password": "12345678901234"},
    )
    # Intento de login con distinto email
    response_diferent_email = client.post(
        "/auth/login",
        data={"username": "dist@gmail.com", "password": "12345678901234"},
    )
    # intento de login con campo 'email' vacio
    response_empty_email = client.post(
        "/auth/login",
        data={"username": "", "password": "12345678901234"},
    )
    assert response_diferent_email.status_code == 401
    assert response_empty_email.status_code == 422


def test_login_invalid_password(client):
    client.post(
        "/auth/register",
        json={"email": "ana@gmail.com", "password": "12345678901234"},
    )
    response_diferent_password = client.post(
        "/auth/login",
        data={"username": "ana@gmail.com", "password": "123456789012343124124"},
    )
    response_empty_password = client.post(
        "/auth/login",
        data={"username": "ana@gmail.com", "password": ""},
    )
    assert response_diferent_password.status_code == 401
    assert response_empty_password.status_code == 422


def test_login_rate_limit_exceed(client):

    client.post(
        "/auth/register",
        json={"email": "ana@gmail.com", "password": "12345678901234"},
    )
    # 3 intentos de login , deben ser OK
    for _ in range(3):
        response = client.post(
            "/auth/login",
            data={"username": "ana@gmail.com", "password": "12345678901234"},
        )
        assert response.status_code == 200
    # 4 debe dar error
    response = client.post(
        "/auth/login",
        data={"username": "ana@gmail.com", "password": "12345678901234"},
    )
    assert response.status_code == 429
    assert "Rate limit exceeded: 3 per 1 minute" in response.text
