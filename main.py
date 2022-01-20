import json
import os

from datetime import datetime
from fastapi import FastAPI, status

from util import PredictionBody, fetch_data, get_region_data, ModelLibrary
from dotenv import load_dotenv

from ml import *

load_dotenv()

app = FastAPI()

MODEL_LIBRARY = ModelLibrary(int(os.getenv("LIBRARY_SIZE")))


@app.get("/")
async def root() :
    return {"message" : "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str) :
    return {"message" : f"Hello {name}"}
