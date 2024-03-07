#some imports are at the end of the file to avoid circular import problems)
#system import
from __future__ import annotations

# libs import
from pydantic import BaseModel


class CreatePlanning(BaseModel):
    company : 'CreateCompany'
    activities : list[CreateActivity]

class Planning(CreatePlanning):
    id: int
    
#local imports (here to avoid circular import problems)
from models.companies import CreateCompany
from models.activities import CreateActivity