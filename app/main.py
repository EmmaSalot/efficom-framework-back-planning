# Libs imports
from fastapi import FastAPI
from pydantic import BaseModel

#local imports
from routers.users import router as user_router
from routers.companies import router as company_router
from database import initialize_database
from database import get_users_collection

app = FastAPI()
app.include_router(user_router, tags=["Users"])
app.include_router(company_router, tags=["Companies"])

# Initialize the database connection
initialize_database() 

