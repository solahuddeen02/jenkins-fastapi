# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "Hello from FastAPI with Jenkins & SonarQube!"}

def test_average_success():
    r = client.get("/average?numbers=10&numbers=20&numbers=30")
    assert r.status_code == 200
    assert r.json()["average"] == 20.0

def test_average_empty_list_should_422():
    r = client.get("/average")
    assert r.status_code == 422  # missing required query

def test_reverse_string():
    r = client.get("/reverse?text=SonarQube")
    assert r.status_code == 200
    assert r.json()["reversed"] == "ebuQranoS"
