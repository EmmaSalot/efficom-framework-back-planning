# models/users.py

from __future__ import annotations
from pydantic import BaseModel, EmailStr, Field
from typing import List

class UserBase(BaseModel):
    surname: str
    name: str
    email: EmailStr

class CreateUser(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str

class User(UserInDB):
    id: str = Field(None, alias='_id')  # Utilisez 'alias' pour la correspondance avec MongoDB '_id'
    company: 'CreateCompany'
    activities: List['CreateActivity']


from models.activities import CreateActivity 
from models.companies import CreateCompany
# Faites de même pour vos autres modèles si nécessaire...
