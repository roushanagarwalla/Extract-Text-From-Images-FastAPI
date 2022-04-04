from fastapi import Depends, FastAPI, HTTPException, Header, UploadFile, File, status
from fastapi.responses import FileResponse
import pytesseract
import pathlib, io, uuid, os
from PIL import Image
from .config import Settings, get_settings

app = FastAPI()

settings = get_settings()
BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = pathlib.Path.joinpath(BASE_DIR, "upload")
DEBUG = settings.DEBUG

@app.get("/")
def hello():
    return {"Hello": "World"}

def verify_auth(authorization: Header(None), settings: Settings = Depends(get_settings)):
    if settings.SKIP_AUTH and settings.DEBUG:
        return
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization")

    try:
        label, token = authorization.split()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Either label or Token is missing")

    if token != settings.AUTH_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization")


@app.post("/")
async def make_predictions(file: UploadFile = File(...), authorization_token = Header(None), settings: Settings = Depends(get_settings)):
    verify_auth(authorization_token, settings)
    bytes_str = io.BytesIO(await file.read())
    try:
        img = Image.open(bytes_str)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Image")
    pred = pytesseract.image_to_string(img)
    predictions = [x for x in pred.strip().split("\n")]
    return {"data": predictions, "original": pred}


@app.post("/image-echo", response_class=FileResponse)
async def image_echo_view(file: UploadFile = File(...), settings: Settings = Depends(get_settings)):
    if not os.path.exists(UPLOAD_DIR):
        os.mkdir(UPLOAD_DIR)
    if not settings.ECHO_ACTIVE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Endpoint")
    bytes_str = io.BytesIO(await file.read())
    try:
        img = Image.open(bytes_str)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Image")

    fname = pathlib.Path(file.filename)
    fext = fname.suffix
    dest = UPLOAD_DIR / f"{uuid.uuid1()}{fext}"
    img.save(dest)
    return dest