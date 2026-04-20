def test_logout_success(authed_client):
    response = authed_client.post("/auth/logout")
    assert response.status_code == 200
    assert (
        "access_token" not in response.cookies
        or response.cookies.get("access_token") == ""
    )


def test_logout_without_auth(client):
    response = client.post("/auth/logout")
    assert response.status_code == 401
