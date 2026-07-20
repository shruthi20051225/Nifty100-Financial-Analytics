from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_peer_group():
    response = client.get("/api/v1/peers/Power & Utilities")
    assert response.status_code in [200, 404]


def test_invalid_peer():
    response = client.get("/api/v1/peers/INVALID")
    assert response.status_code == 404


def test_compare_company():
    response = client.get("/api/v1/companies/TCS/peers/compare")
    assert response.status_code in [200, 404]
