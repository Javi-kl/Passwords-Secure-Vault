import jwt


def test_me_with_valid_cookie(authed_client):
    """
    Usa fixture authed_client que tiene la cookie del login.
    GET /auth/me para verificar que devuelve los datos del usuario.
    """
    response = authed_client.get("/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@test.com"
    assert "id" in data


def test_me_without_cookie(client):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_me_with_invalid_token(client):
    # crear un token con una clave falsa
    fake_token = jwt.encode({"sub": "test@test.com"}, "clave_falsa", algorithm="HS256")
    client.cookies.set("access_token", fake_token)
    response = client.get("/auth/me")
    assert response.status_code == 401
