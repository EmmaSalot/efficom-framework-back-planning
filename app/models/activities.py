#some imports are at the end of the file to avoid circular import problems)
# libs import
from pydantic import BaseModel

class CreateActivity(BaseModel):
    day : str
    start : str
    end: str
    planning : CreatePlanning

class Activity(CreateActivity):
    id: int
  
#local imports (here to avoid circular import problems)
from models.plannings import CreatePlanning