# libs import
from pydantic import BaseModel

class CreateActivity(BaseModel):
    day : str
    start : str
    end: str

class Activity(CreateActivity):
    id: int