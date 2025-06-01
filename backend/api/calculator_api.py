import os

import joblib
from fastapi import APIRouter
from fastapi import Request
from pandas import DataFrame
from tinydb import TinyDB, Query
from datetime import datetime

from calculator.calculator import Calculator

router = APIRouter(
    prefix="/calculator",
    tags=["calculator"]
)

db = TinyDB('database.json')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'rf_model.joblib')
rf_model = joblib.load(file_path)


@router.post("/calculate/{year}")
async def calculate(year: int, request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}

    # Parse input data
    input = {k: v for k, v in data.items() if v != ""}

    calculator = Calculator(input)
    result = calculator.to_result_dict(int(year))

    result['code'] = 123456
    result['notes'] = []
    result['contact_people'] = []
    result['tasks'] = []

    result['id'] = db.insert(result)

    return result


@router.post("/estimate")
async def estimate(request: Request):
    data = await request.json()

    print(rf_model.feature_names_in_)
    new_data = DataFrame({
        "NCOMBATH": [int(data.get("ncombath"))],
        "TOTROOMS": [int(data.get("totrooms"))],
        "NHSLDMEM": [int(data.get("nhsldmem"))],
        "ATHOME": [int(data.get("athome"))],
        "AIRCOND": [int(data.get("aircond"))],
        "HIGHCEIL": [int(data.get("highceil"))],
        "NUM_DEVICES": [int(data.get("num_devices"))],
    })
    print(new_data)
    predicted_kwh = rf_model.predict(new_data)

    return {"predicted_kwh": round(predicted_kwh[0], 2)}


@router.get("/result/{result_id}")
async def get_result(result_id: int):
    result = db.get(doc_id=result_id)
    if not result:
        return {"error": "Not found"}
    return result


@router.post("/result/{result_id}/note")
async def add_note(result_id: int, request: Request):
    data = await request.json()
    note = {
        "name": data.get("name"),
        "description": data.get("description"),
        "created_at": datetime.utcnow().isoformat()
    }
    db.update(lambda r: r["notes"].append(note), doc_ids=[result_id])
    return {"success": True, "note": note}


@router.delete("/result/{result_id}/note/{note_idx}")
async def delete_note(result_id: int, note_idx: int):
    def remove_note(record):
        if 0 <= note_idx < len(record["notes"]):
            record["notes"].pop(note_idx)
        return record

    db.update(remove_note, doc_ids=[result_id])
    return {"success": True}


@router.post("/result/{result_id}/contact")
async def add_contact(result_id: int, request: Request):
    data = await request.json()
    contact = {
        "name": data.get("name"),
        "phone": data.get("phone"),
        "mail": data.get("mail"),
        "position": data.get("position")
    }
    db.update(lambda r: r["contact_people"].append(contact), doc_ids=[result_id])
    return {"success": True, "contact": contact}


@router.delete("/result/{result_id}/contact/{contact_idx}")
async def delete_contact(result_id: int, contact_idx: int):
    def remove_contact(record):
        if 0 <= contact_idx < len(record["contact_people"]):
            record["contact_people"].pop(contact_idx)
        return record

    db.update(remove_contact, doc_ids=[result_id])
    return {"success": True}


@router.post("/result/{result_id}/task")
async def add_task(result_id: int, request: Request):
    data = await request.json()
    task = {
        "name": data.get("name"),
        "description": data.get("description"),
        "deadline": data.get("deadline"),  # oczekuj ISO stringa od klienta
        "created_at": datetime.utcnow().isoformat(),
        "ended": False
    }
    db.update(lambda r: r["tasks"].append(task), doc_ids=[result_id])
    return {"success": True, "task": task}


@router.delete("/result/{result_id}/task/{task_idx}")
async def delete_task(result_id: int, task_idx: int):
    def remove_task(record):
        if 0 <= task_idx < len(record["tasks"]):
            record["tasks"].pop(task_idx)
        return record

    db.update(remove_task, doc_ids=[result_id])
    return {"success": True}


@router.post("/result/{result_id}/task/{task_idx}/end")
async def end_task(result_id: int, task_idx: int):
    def finish_task(record):
        if 0 <= task_idx < len(record["tasks"]):
            record["tasks"][task_idx]["ended"] = True
        return record

    db.update(finish_task, doc_ids=[result_id])
    return {"success": True}
