def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={"email": "ana@gmail.com", "password": "UnaClaveSegura2024!"},
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
        json={"email": "ana@gmail.com", "password": "UnaClaveSegura2024!"},
    )
    response = client.post(
        "/auth/register",
        json={"email": "ana@gmail.com", "password": "OtraClaveDistinta2024!"},
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
        json={"email": "no-es-email", "password": "UnaClaveSegura2024"},
    )
    assert response.status_code == 422


def test_register_empty_body(client):
    response = client.post("/auth/register", json={})
    assert response.status_code == 422


def test_register_rate_limit_exceed(client):
    count = 100
    for _ in range(3):
        email_user = str(count) + "@gmail.com"
        response = client.post(
            "/auth/register",
            json={"email": email_user, "password": "UnaClaveSegura2024"},
        )
        count += 1
        assert response.status_code == 201
    # 4 debe dar error
    response = client.post(
        "/auth/register",
        json={"email": "ana@gmail.com", "password": "OtraClave12345!"},
    )

    assert response.status_code == 429
    assert "Rate limit exceeded: 3 per 1 minute" in response.text


def test_register_weak_password_rejected_by_zxcvbn(client):
    """Contraseñas con score zxcvbn < 2 son rechazadas con 422."""
    # score 0: secuencia de teclado de 14 caracteres
    response = client.post(
        "/auth/register",
        json={"email": "test@test.com", "password": "qwertyuiopasdfg"},
    )
    assert response.status_code == 422
    assert "no es lo suficientemente segura" in response.text.lower()


def test_register_strong_password_accepted(client):
    """Contraseñas con score zxcvbn >= 2 y len >= 14 son aceptadas."""
    response = client.post(
        "/auth/register",
        json={"email": "fuerte@test.com", "password": "UnaClaveSegura2024!"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "fuerte@test.com"
