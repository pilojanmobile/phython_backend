from pydantic import BaseModel, EmailStr

class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    role: str


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True