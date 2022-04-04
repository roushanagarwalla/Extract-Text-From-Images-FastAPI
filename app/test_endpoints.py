from fastapi.testclient import TestClient
from app.main import app
import pathlib
import time, shutil

BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "upload"

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

def test_echo_images():
    images_path = BASE_DIR / "test_data" / "images"
    content_types_list = ["image/jpeg", "image/png"]
    for path in images_path.glob("*"):
        response = client.post("/image-echo", files={"file": open(path, "rb")})
        assert response.status_code == 200
        assert response.headers['content-type'] in content_types_list
        time.sleep(3)
        shutil.rmtree(UPLOAD_DIR)