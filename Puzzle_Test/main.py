from fastapi import FastAPI, HTTPException
import json
from pathlib import Path

app = FastAPI(title="Employee Management API")

EMPLOYEE_FILE = Path("employees.json")


def load_employees():
    if not EMPLOYEE_FILE.exists():
        return []
    with open(EMPLOYEE_FILE, "r") as f:
        return json.load(f)

def save_employees(employees):
    with open(EMPLOYEE_FILE, "w") as f:
        json.dump(employees, f, indent=4)


@app.get("/")
def root():
    return {"message": "Welcome to the Employee Management API!"}


# ---------------------------
# READ – Get a single employee
# ---------------------------
@app.get("/employees/{employeeId}")
def get_employee(employeeId: int):
    employees = load_employees()

    for employee in employees:
        if employee.get("employeeId") == employeeId:
            return employee

    raise HTTPException(status_code=404, detail="Employee not found")


# ---------------------------
# READ – Get all employees
# ---------------------------
@app.get("/employees")
def list_employees():
    return load_employees()