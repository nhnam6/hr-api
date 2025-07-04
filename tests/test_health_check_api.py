"""Test health check API"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check():
    """Test health check"""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert data["message"] == "Service is healthy"
