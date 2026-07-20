from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_health_status():

    response = client.get("/api/v1/health")

    assert response.status_code == 200


def test_health_response():

    response = client.get("/api/v1/health")

    data = response.json()

    assert "status" in data

    assert data["status"] == "ok"


def test_database_counts():

    response = client.get("/api/v1/health")

    data = response.json()

    assert "db_row_counts" in data


def test_version_exists():

    response = client.get("/api/v1/health")

    data = response.json()

    assert "version" in data
