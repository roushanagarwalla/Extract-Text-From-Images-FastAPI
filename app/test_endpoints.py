import io
from fastapi.testclient import TestClient
from app.main import app
import pathlib
import time, shutil
from PIL import Image
from .config import get_settings

settings = get_settings()

BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "upload"

client = TestClient(app)

def test_get_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers['content-type'] == "application/json"
    assert response.json() == {"Hello": "World"}

def test_echo_images():
    if settings.ECHO_ACTIVE:
        images_path = BASE_DIR / "test_data" / "images"
        content_types_list = ["image/jpeg", "image/png"]
        for path in images_path.glob("*"):
            response = client.post("/image-echo", files={"file": open(path, "rb")})
            try:
                img = Image.open(path)
            except:
                img = None

            if img is None:
                assert response.status_code == 400
            else:
                assert response.status_code == 200
                assert response.headers['content-type'] in content_types_list

            time.sleep(2)
            shutil.rmtree(UPLOAD_DIR)

def test_predictions():
    response = client.post("/")
    assert response.status_code == 422
    images_path = BASE_DIR / "test_data" / "images"
    for path in images_path.glob("*"):
        response = client.post("/", files={"file": open(path, "rb")})
        try:
            img = Image.open(path)
        except:
            img = None

        if img is None:
            assert response.status_code == 400
        else:
            assert response.status_code == 200
            assert response.headers['content-type'] == "application/json"
            assert len(response.json().keys()) == 2