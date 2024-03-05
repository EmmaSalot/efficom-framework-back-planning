# libs import
from pydantic import BaseModel
from companies import CreateCompany
from activities import CreateActivity
from typing import List

class CreateUser(BaseModel):
    surname : str
    name : str
    email: str
    password: str
    company : CreateCompany
    activities : List[CreateActivity]

class User(CreateUser):
    id: int