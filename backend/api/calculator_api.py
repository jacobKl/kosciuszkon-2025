from fastapi import APIRouter
from fastapi import Request

from calculator.calculator import Calculator

router = APIRouter(
    prefix="/calculator",
    tags=["calculator"]
)


@router.post("/calculate/{year}")
async def calculate(year: int, request: Request):
    data = await request.json()

    # Parse input data
    # TODO
    input = data
    print(data)

    calculator = Calculator(input)

    return calculator.to_result_dict(int(year))


@router.post("/estimate")
async def estimate(data):
    print(data)
