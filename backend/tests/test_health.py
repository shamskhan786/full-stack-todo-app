from unittest.mock import patch

from fastapi.testclient import TestClient


def test_health_check_healthy(client: TestClient):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"


def test_health_check_no_auth_required(client_no_auth: TestClient):
    """Health check should work without any authentication."""
    response = client_no_auth.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_health_check_db_failure(client: TestClient):
    """When DB is unreachable, health check returns 503."""
    with patch("src.api.health.engine") as mock_engine:
        mock_engine.connect.return_value.__enter__ = lambda s: s
        mock_engine.connect.return_value.__exit__ = lambda s, *a: None
        mock_engine.connect.side_effect = Exception("Connection refused")
        response = client.get("/api/health")
        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["database"] == "disconnected"
