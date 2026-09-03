from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


def test_health_database_returns_200(client: TestClient):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health__database_down_returns_503(client: TestClient, monkeypatch):
    def broken_ping(db):
        raise SQLAlchemyError("connection refused")

    monkeypatch.setattr("app.routers.health_router.ping", broken_ping)

    response = client.get("/health")

    assert response.status_code == 503
