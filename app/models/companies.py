#some imports are at the end of the file to avoid circular import problems)
#system imports
from __future__ import annotations

# libs imports
from pydantic import BaseModel, Field
from typing import List

class CreateCompany(BaseModel):
    name: str | None = None
    address: str| None = None
    plannings: List['CreatePlanning'] | None = None

class Company(CreateCompany):
    id: str = Field(None, alias='_id')

from models.plannings import CreatePlanning  # Assurez-vous que ce modèle existe