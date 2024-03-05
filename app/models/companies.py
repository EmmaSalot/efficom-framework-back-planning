# libs import
from typing import List
from pydantic import BaseModel
from users import CreateUser
from activities import CreateActivity

class CreateCompany(BaseModel):
    name: str
    address : str
    users : List[CreateUser]
    planning : List[CreateActivity]

class Company(CreateCompany):
    id: int