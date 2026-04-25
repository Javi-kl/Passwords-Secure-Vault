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
    assert "access_token" in response.cookies


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
    # 5 intentos de login , deben ser OK
    for _ in range(5):
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
    assert "Rate limit exceeded: 5 per 1 minute" in response.text


def test_login_generic_error_message(client):
    """el sistema no debe revelar si falló por email inexistente o contraseña incorrecta."""
    client.post(
        "/auth/register", json={"email": "ana@gmail.com", "password": "12345678901234"}
    )
    # Email que no existe
    response_wrong_email = client.post(
        "/auth/login",
        data={"username": "noexiste@gmail.com", "password": "12345678901234"},
    )
    # Contraseña incorrecta
    response_wrong_password = client.post(
        "/auth/login",
        data={"username": "ana@gmail.com", "password": "incorrecta1234567"},
    )
    assert response_wrong_email.status_code == 401
    assert response_wrong_password.status_code == 401
    # Ambos errores deben tener exactamente el mismo mensaje
    assert (
        response_wrong_email.json()["detail"]
        == response_wrong_password.json()["detail"]
    )
