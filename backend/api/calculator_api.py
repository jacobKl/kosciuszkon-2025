import os

import joblib
from fastapi import APIRouter
from fastapi import Request
from pandas import DataFrame

from calculator.calculator import Calculator

router = APIRouter(
    prefix="/calculator",
    tags=["calculator"]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'rf_model.joblib')
rf_model = joblib.load(file_path)


@router.post("/calculate/{year}")
async def calculate(year: int, request: Request):
    data = await request.json()

    # Parse input data
    input = {k: v for k, v in data.items() if v != ""}

    calculator = Calculator(input)

    return calculator.to_result_dict(int(year))


@router.post("/estimate")
async def estimate(request: Request):
    data = await request.json()

    new_data = DataFrame({
        "NCOMBATH": [int(data.get("ncombath"))],
        "TOTROOMS": [int(data.get("totrooms"))],
        "NHSLDMEM": [int(data.get("nhsldmem"))],
        "ATHOME": [int(data.get("athome"))],
        "NUM_DEVICES": [int(data.get("num_devices"))]
    })
    predicted_kwh = rf_model.predict(new_data)

    return {"predicted_kwh": round(predicted_kwh[0], 2)}
