import os
from datetime import datetime, timedelta, date
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, status, HTTPException

from ml import *
from util import ModelLibrary, InvalidParameter, check_all
from util.data_retrieval import fetch_data, get_nation_data, get_region_data

load_dotenv()

app = FastAPI()

MODEL_LIBRARY = ModelLibrary(int(os.getenv("LIBRARY_SIZE")))


@app.get("/")
async def root() :
    return {"message" : "Hello World"}

# @app.get("/hello/{name}")
# async def say_hello(name : str) :
#     return {"message" : f"Hello {name}"}


@app.get("/api/v1/covid/update/", status_code = status.HTTP_204_NO_CONTENT)
async def update() :
    # Update region data
    overall_data = fetch_data(os.getenv("COV_NAT_DATA_URL"))
    nation_data  = get_nation_data(overall_data)["P"]

    # Create model
    model = SarimaxModel("FRA")
    model.fit(nation_data)
    model.save()


@app.get("/api/v1/covid/update/{region}", status_code = status.HTTP_204_NO_CONTENT)
async def update_regional_model(region : str) :
    # Update region data
    overall_data = fetch_data(os.getenv("COV_REG_DATA_URL"))
    region_data  = get_region_data(overall_data, [region])[region]["P"]

    # Create Model
    model = SarimaxModel(region)
    model.fit(region_data)
    model.save()


@app.get("/api/v1/covid/predict", status_code = status.HTTP_200_OK)
async def predict(start_date : date = datetime.today().date() - timedelta(days = 3),
                  end_date : date = datetime.today().date() + timedelta(days = 6),
                  region : str = "FRA") :

    invalids : List[InvalidParameter] = check_all(start_date, end_date, region, prediction = True)

    if len(invalids) > 0 :
        message = [[param.field, param.message] for param in invalids]
        raise HTTPException(status_code = 400,
                            detail = message)

    # Load model
    model = SarimaxModel(region)

    # Check if model is in library
    if (lib_model := MODEL_LIBRARY.get_model(model.file_root)) is None :
        model.load()
        MODEL_LIBRARY.add_model(model)
    else :
        model = lib_model

    # Make prediction
    prediction = model.predict(start_date, end_date)

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


@app.get("/api/v1/covid/data", status_code = status.HTTP_200_OK)
async def get_all_data(start_date : date = "2020-06-01",
                       end_date : date = datetime.today().date(),
                       region : str = "FRA") :

    invalids : List[InvalidParameter] = check_all(start_date, end_date, region, prediction = False)

    if len(invalids) > 0 :
        message = [[param.field, param.message] for param in invalids]
        raise HTTPException(status_code = 400,
                            detail = message)

    # Get existing (true) data

    end_date = datetime(end_date.year, end_date.month, end_date.day)
    start_date = datetime(start_date.year, start_date.month, start_date.day)

    if region == "FRA" :
        data = get_nation_data(fetch_data(os.getenv("COV_NAT_DATA_URL")))
    else :
        data = get_region_data(fetch_data(os.getenv("COV_REG_DATA_URL")), [region])[region]

    data = data["P"]

    model = SarimaxModel(region)

    # Check if model is in library
    if (lib_model := MODEL_LIBRARY.get_model(model.file_root)) is None :
        model.load()
        MODEL_LIBRARY.add_model(model)
    else :
        model = lib_model

    true_end = min(end_date, model.last_true_date)

    existing_data = data.loc[(data.index <= true_end) & (data.index >= start_date)]
    data_points = [
        {
            "date" : index.to_pydatetime().strftime("%Y-%m-%d"),
            "cases" : int(value),
            "predicted" : False
        }
        for index, value in existing_data.items()
    ]

    if end_date > true_end :
        first_prediction = true_end + timedelta(days = 1)
        predictions = model.predict(start = first_prediction.date(), end = end_date.date())

        data_points += [
            {
                "date" : index.to_pydatetime().strftime("%Y-%m-%d"),
                "cases" : int(value),
                "predicted" : True
            }
            for index, value in predictions.items()
        ]

    return {"status" : "OK",
            "body" : {
                "data" : data_points
            }}
