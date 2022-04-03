from fastapi import FastAPI

from .config import get_settings

app = FastAPI()

settings = get_settings()

DEBUG = settings.DEBUG

@app.get("/")
def hello():
    return {"Hello": "World"}

@app.post("/")
def hello_post():
    return {"message": "Hello World"}
