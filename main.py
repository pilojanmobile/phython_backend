from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

class Employee(BaseModel):
    id:int
    name:str
    age:int

employee_list = []

@app.get("/")
async def Home():
    return {'message' : "Working fine"}

@app.get("/api/employees")
def get_employees():
    return {
        "success": True,
        "employees": employee_list
    }    

@app.post("/api/add_employee")
def add_employee(employee: Employee):
    employee.id = len(employee_list) + 1
    employee_list.append(employee)
    return {
        "success": True,
        "message": "Employee added successfully"
    }             

@app.delete("/api/delete_employee/{employee_id}")
def delete_employee(employee_id: int):
    for employee in employee_list:
        if employee.id == employee_id:
            employee_list.remove(employee)
            return {
                "success": True,
                "message": "Employee deleted successfully"
            }
    return {
        "success": False,
        "message": "Employee not found"
    }

@app.put("/api/update_employee/{employee_id}")
def update_employee(employee_id: int, employee: Employee):

    for index, existing_employee in enumerate(employee_list):

        if existing_employee.id == employee_id:

            employee.id = employee_id
            employee_list[index] = employee

            return {
                "success": True,
                "message": "Employee updated successfully",
                "employee": employee
            }

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )

