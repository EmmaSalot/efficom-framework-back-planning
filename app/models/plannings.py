# libs import
from pydantic import BaseModel
from companies import CreateCompany
from activities import CreateActivity
from typing import List

class CreatePlanning(BaseModel):
    company : CreateCompany
    activities : List[CreateActivity]

class Planning(CreatePlanning):
    id: int