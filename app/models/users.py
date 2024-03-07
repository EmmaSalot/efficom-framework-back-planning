#some imports are at the end of the file to avoid circular import problems)
#system imports
from __future__ import annotations

#lib imports
from pydantic import BaseModel, EmailStr, Field, SecretStr
from typing import List

class UserRegistration(BaseModel):
    name: str| None = None
    email: EmailStr| None = None
    password: SecretStr  # Utilisez SecretStr pour une meilleure sécurité
    company : str 

class User(BaseModel):
    id: str = Field(None, alias='_id')
    surname: str| None = None
    name: str| None = None
    email: EmailStr| None = None
    hashed_password: str| None = None
    company: str | None = None  # Assumez un simple champ string pour l'exemple, ajustez selon votre modèle
    activities: List['CreateActivity']| None = None

    # Méthode pour cacher le mot de passe haché dans les sorties
    def dict(self, **kwargs):
        user_dict = super().dict(**kwargs)
        user_dict.pop("hashed_password")
        return user_dict
   
      
#local imports (here to avoid circular import problems)
from models.activities import CreateActivity
from models.companies import CreateCompany

