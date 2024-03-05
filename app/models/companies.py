#system imports
from __future__ import annotations

# libs imports
from pydantic import BaseModel

class CreateCompany(BaseModel):
    name: str 
    address : str | None = None
    users : list[CreateUser] | None = None
    planning : list[CreateActivity] | None = None

class Company(CreateCompany):
    _id: int | None = None

#local imports (here to avoid circular import problems)
from models.users import CreateUser
from models.activities import CreateActivity