from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_all_sectors():
    response = client.get("/api/v1/sectors")
    assert response.status_code == 200


def test_financials_sector():
    response = client.get("/api/v1/sectors/Financials/companies")
    assert response.status_code in [200, 404]


def test_it_sector():
    response = client.get("/api/v1/sectors/Information Technology/companies")
    assert response.status_code in [200, 404]


def test_energy_sector():
    response = client.get("/api/v1/sectors/Energy/companies")
    assert response.status_code in [200, 404]
