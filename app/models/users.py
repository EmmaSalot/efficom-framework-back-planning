#some imports are at the end of the file to avoid circular import problems)
#system imports
from __future__ import annotations

#lib imports
from pydantic import BaseModel, EmailStr, Field
from typing import List

class UserBase(BaseModel):
    surname: str
    name: str
    email: EmailStr

class CreateUser(BaseModel):
    surname : str | None = None
    name : str | None = None
    email: str | None = None
    password: str | None = None
    company : CreateCompany | None = None
    activities : list[CreateActivity] | None = None

class User(CreateUser):
    _id: str

class CreateUser(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str

class User(UserInDB):
    id: str = Field(None, alias='_id')  # Utilisez 'alias' pour la correspondance avec MongoDB '_id'
    company: 'CreateCompany'
    activities: List['CreateActivity']
      
#local imports (here to avoid circular import problems)
from models.activities import CreateActivity
from models.companies import CreateCompany

