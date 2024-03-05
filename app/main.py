# Libs imports
from fastapi import FastAPI
from pydantic import BaseModel

#local imports
from routers.users import router as user_router
from database import initialize_database

app = FastAPI()
app.include_router(user_router, tags=["Users"])

# Initialize the database connection
initialize_database() 

