from database import engine, Base
from models import EmployeeDB

# Create database tables
Base.metadata.create_all(bind=engine)

print("Employee table created successfully!")