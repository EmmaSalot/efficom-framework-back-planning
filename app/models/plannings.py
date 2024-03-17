#some imports are at the end of the file to avoid circular import problems)
# System import
from __future__ import annotations

# Libs import
from pydantic import BaseModel, Field
from typing import List

# Define the CreatePlanning model
class CreatePlanning(BaseModel):
    company: str | None = None
    activities: List['CreateActivity'] | None = None

class Planning(CreatePlanning):
    id: str = Field(None, alias='_id')

# Local import to avoid circular import problems
from models.activities import CreateActivity
