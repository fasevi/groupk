from fastapi import FastAPI, HTTPException
import json
from pathlib import Path

app = FastAPI(title="Employee Management API")

# Prefer employees.json next to this module; fall back to repo root
module_dir = Path(__file__).resolve().parent
local_file = module_dir / "employees.json"
root_file = module_dir.parent / "employees.json"
EMPLOYEES_FILE = local_file if local_file.exists() else root_file


def load_employees():
    if not EMPLOYEES_FILE.exists():
        return []
    try:
        with open(EMPLOYEES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="employees.json is not valid JSON")


@app.get("/")
def root():
    return {"message": "Welcome to the Employee Management API!"}


@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    employees = load_employees()
    for employee in employees:
        if employee.get("employeeId") == employee_id or employee.get("id") == employee_id:
            return employee
    raise HTTPException(status_code=404, detail="Employee not found")


@app.get("/employees")
def list_employees():
    return load_employees()
