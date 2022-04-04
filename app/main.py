from fastapi import Depends, FastAPI, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse

import pathlib, io, uuid, os

from .config import Settings, get_settings

app = FastAPI()

settings = get_settings()

BASE_DIR = pathlib.Path(__file__).parent

UPLOAD_DIR = pathlib.Path.joinpath(BASE_DIR, "upload")

if not os.path.exists(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)

DEBUG = settings.DEBUG

@app.get("/")
def hello():
    return {"Hello": "World"}

@app.post("/")
def hello_post():
    return {"message": "Hello World"}


@app.post("/image-echo", response_class=FileResponse)
async def image_echo_view(file: UploadFile = File(...), settings: Settings = Depends(get_settings)):
    if not settings.ECHO_ACTIVE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Endpoint")
    bytes_str = io.BytesIO(await file.read())
    fname = pathlib.Path(file.filename)
    fext = fname.suffix
    dest = UPLOAD_DIR / f"{uuid.uuid1()}{fext}"
    with open(dest, "wb") as f:
        f.write(bytes_str.read())
    return dest