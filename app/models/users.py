#system imports
from __future__ import annotations

# libs import
from pydantic import BaseModel


class CreateUser(BaseModel):
    surname : str
    name : str
    email: str
    password: str
    company : CreateCompany
    activities : list[CreateActivity]

class User(CreateUser):
    id: int
    
#local imports (here to avoid circular import problems)
from models.activities import CreateActivity
from models.companies import CreateCompany