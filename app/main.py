from fastapi import Depends, FastAPI, HTTPException, UploadFile, File, status
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

@app.post("/")
async def make_predictions(file: UploadFile = File(...), settings: Settings = Depends(get_settings)):
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