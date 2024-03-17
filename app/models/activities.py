#some imports are at the end of the file to avoid circular import problems)
#system import
from __future__ import annotations
# libs import
from pydantic import BaseModel, Field
from typing import Optional

class CreateActivity(BaseModel):
    day: str
    start: str
    end: str
    planning: CreatePlanning | None = None

class Activity(CreateActivity):
    id: str = Field(None, alias='_id')

# Local import to avoid circular import problems
from models.plannings import CreatePlanning
