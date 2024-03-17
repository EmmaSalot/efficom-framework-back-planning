#some imports are at the end of the file to avoid circular import problems)
#system import
from __future__ import annotations

# libs import
from pydantic import BaseModel, Field
from typing import List

class CreatePlanning(BaseModel):
    # Utilisation d'une référence en avant et rendu optionnel pour éviter une dépendance circulaire directe
    company: str | None = None
    # Liste de références en avant pour les activités
    activities: List['CreateActivity'] | None = None

class Planning(CreatePlanning):
    id: str = Field(None, alias='_id')

# Les importations locales sont reportées après les définitions des classes
from models.activities import CreateActivity  # Assurez-vous que ce modèle existe