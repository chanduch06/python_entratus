from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_fetch_data():
    response = client.get("/fetch_data?city=London")
    assert response.status_code == 200

def test_get_results():
    response = client.get("/results")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
