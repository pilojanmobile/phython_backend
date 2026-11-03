from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import EmployeeDB
from schemas import EmployeeCreate, EmployeeResponse

from database import engine, Base
from contextlib import asynccontextmanager





@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database tables...")

    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully!")

    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"message": "FastAPI PostgreSQL Backend"}


# POST - Add employee
@app.post("/api/add_employee")
def add_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):

    new_employee = EmployeeDB(
        name=employee.name,
        email=employee.email,
        role=employee.role
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return {
        "success": True,
        "message": "Employee added successfully",
        "employee": new_employee
    }


# GET - Get all employees
@app.get("/api/get_employees")
def get_employees(db: Session = Depends(get_db)):

    employees = db.query(EmployeeDB).all()

    return employees


# GET - Get one employee
@app.get("/api/get_employee/{employee_id}")
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = db.query(EmployeeDB).filter(
        EmployeeDB.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


# PUT - Update employee
@app.put("/api/update_employee/{employee_id}")
def update_employee(
    employee_id: int,
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):

    existing_employee = db.query(EmployeeDB).filter(
        EmployeeDB.id == employee_id
    ).first()

    if not existing_employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    existing_employee.name = employee.name
    existing_employee.email = employee.email
    existing_employee.role = employee.role

    db.commit()
    db.refresh(existing_employee)

    return {
        "success": True,
        "message": "Employee updated successfully"
    }


# DELETE - Delete employee
@app.delete("/api/delete_employee/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = db.query(EmployeeDB).filter(
        EmployeeDB.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db.delete(employee)
    db.commit()

    return {
        "success": True,
        "message": "Employee deleted successfully"
    }