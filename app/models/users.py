#system imports
from __future__ import annotations

# libs import
from pydantic import BaseModel


class CreateUser(BaseModel):
    surname : str | None = None
    name : str | None = None
    email: str | None = None
    password: str | None = None
    company : CreateCompany | None = None
    activities : list[CreateActivity] | None = None

class User(CreateUser):
    _id: str
    
#local imports (here to avoid circular import problems)
from models.activities import CreateActivity
from models.companies import CreateCompany