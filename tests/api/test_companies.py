from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_company_list():

    response = client.get("/api/v1/companies")

    assert response.status_code == 200

    assert isinstance(response.json(), list)


def test_company_profile():

    response = client.get("/api/v1/companies/TCS")

    assert response.status_code in [200, 404]


def test_company_ratios():

    response = client.get("/api/v1/companies/TCS/ratios")

    assert response.status_code in [200, 404]


def test_company_pl():

    response = client.get("/api/v1/companies/TCS/pl")

    assert response.status_code in [200, 404]


def test_company_bs():

    response = client.get("/api/v1/companies/TCS/bs")

    assert response.status_code in [200, 404]


def test_company_cashflow():

    response = client.get("/api/v1/companies/TCS/cashflow")

    assert response.status_code in [200, 404]
