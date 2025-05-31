from fastapi import APIRouter

from calculator.calculator import Calculator

router = APIRouter(
    prefix="/calculator",
    tags=["calculator"]
)

@router.post("/calculate/{year}")
async def calculate(year, data=None):
    # Parse input data
    # TODO
    input = data

    calculator = Calculator(input)

    return calculator.to_result_dict(int(year))