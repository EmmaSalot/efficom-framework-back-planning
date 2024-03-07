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
    # Utilisation d'une référence en avant et rendu optionnel
    planning: CreatePlanning | None = None

class Activity(CreateActivity):
    id: str = Field(None, alias='_id')

# Les importations locales sont reportées après les définitions des classes
from models.plannings import CreatePlanning  # Assurez-vous que ce modèle existe
