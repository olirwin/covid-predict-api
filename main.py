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
async def say_hello(name : str) :
    return {"message" : f"Hello {name}"}


@app.get("/api/v1/covid/update/", status_code = status.HTTP_200_OK)
async def update() :
    return {"test ok"}


@app.get("/api/v1/covid/update/{region}", status_code = status.HTTP_204_NO_CONTENT)
async def update_regional_model(region : str) :
    # Update region data
    overall_data = fetch_data(os.getenv("COV_REG_DATA_URL"))
    region_data  = get_region_data(overall_data, [region])[region]["P"]

    # Create Model
    model = SarimaxModel(region)
    model.fit(region_data)
    model.save()


@app.post("/api/v1/covid/predict", status_code = status.HTTP_200_OK)
async def predict(body : PredictionBody) :

    # Load model
    model = SarimaxModel(body.region)

    # Check if model is in library
    if (lib_model := MODEL_LIBRARY.get_model(model.filename)) is None :
        model.load()
        MODEL_LIBRARY.add_model(model)
    else :
        model = lib_model

    # Make prediction
    prediction = model.predict(body.start_date, body.end_date)

    return {"status" : "OK",
            "body" : {
                "predictions" : [
                    {
                        "date" : index.to_pydatetime().strftime("%Y-%m-%d"),
                        "cases" : int(value)
                    }
                    for index, value in prediction.items()
                ]
            }}


@app.get("/api/v1/covid/library", status_code = 200)
async def get_library() :

    resp = {"library" : MODEL_LIBRARY.list_model_names()}

    return resp

