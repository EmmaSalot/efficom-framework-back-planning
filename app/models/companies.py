#system imports
from __future__ import annotations

# libs imports
from pydantic import BaseModel

class CreateCompany(BaseModel):
    name: str
    address : str
    users : list[CreateUser]
    planning : list[CreateActivity]

class Company(CreateCompany):
    id: int

#local imports (here to avoid circular import problems)
from models.users import CreateUser
from models.activities import CreateActivity