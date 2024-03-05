from fastapi import FastAPI
from database import get_database

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/users/")
def add_user():
    
    
    return {"Hello": "World"}