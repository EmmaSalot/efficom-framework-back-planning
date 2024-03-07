#some imports are at the end of the file to avoid circular import problems)
#system imports
from __future__ import annotations

# libs imports
from pydantic import BaseModel

class CreateCompany(BaseModel):
    name: str | None = None
    address : str | None = None
    users : list[CreateUser2] | None = None
    plannings : list[CreatePlanning] | None = None

class Company(CreateCompany):
    _id: str

#local imports (here to avoid circular import problems)
from models.users import CreateUser2
from models.plannings import CreatePlanning