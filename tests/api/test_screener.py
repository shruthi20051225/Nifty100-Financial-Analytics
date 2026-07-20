from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_screener():

    response = client.get("/api/v1/screener")

    assert response.status_code == 200


def test_screener_min_roe():

    response = client.get("/api/v1/screener?min_roe=15")

    assert response.status_code == 200


def test_screener_max_de():

    response = client.get("/api/v1/screener?max_de=1")

    assert response.status_code == 200


def test_screener_sector():

    response = client.get("/api/v1/screener?sector=Financials")

    assert response.status_code == 200
