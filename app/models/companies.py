#system imports
from __future__ import annotations

# libs imports
from pydantic import BaseModel

class CreateCompany(BaseModel):
    name: str | None = None
    address : str | None = None
    users : list[CreateUser] | None = None
    planning : list[CreateActivity] | None = None

class Company(CreateCompany):
    _id: str

#local imports (here to avoid circular import problems)
from models.users import CreateUser
from models.activities import CreateActivity