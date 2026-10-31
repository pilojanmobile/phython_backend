from fastapi import FastAPI

app=FastAPI()


@app.get("/")
async def Home():
    return {'message' : "Working fine"}

@app.get("/api/employees")
def get_employees():
    return {
        "success": True,
        "employees": [
            {
                "id": 1,
                "name": "Pilojan",
                "role": "Software Engineer"
            },
            {
                "id": 2,
                "name": "Employee Two",
                "role": "Developer"
            }
        ]
    }    