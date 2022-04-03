from urllib import response
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers['content-type'] == "application/json"
    assert response.json() == {"Hello": "World"}

def test_post_home():
    response = client.post("/")
    assert response.status_code == 200
    assert response.headers['content-type'] == "application/json"
    assert response.json() == {"message": "Hello World"}
