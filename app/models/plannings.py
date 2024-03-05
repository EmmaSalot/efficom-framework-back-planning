from __future__ import annotations

# libs import
from pydantic import BaseModel


class CreatePlanning(BaseModel):
    company : CreateCompany
    activities : list[CreateActivity]

class Planning(CreatePlanning):
    id: int
    
from models.companies import CreateCompany
from models.activities import CreateActivity