# imports system
from typing import List, Optional

# Libs imports
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId 

# Local imports
from pydantic import SecretStr
from internal import auth
from models.users import User, UserRegistration # Assurez-vous que ce modèle correspond à votre nouveau modèle unifié
from database import get_users_collection, get_companies_collection

router = APIRouter()
users_collection = get_users_collection()
companies_collection = get_companies_collection()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")  # Assurez-vous que cela correspond à votre endpoint de connexion




@router.get("/users", response_model=List[User])
def get_users():
    users = list(users_collection.find())
    # Convertissez les ObjectId en chaînes
    for user in users:
        user["_id"] = str(user["_id"])
    return users

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # Convertissez l'ObjectId en chaîne
    user["_id"] = str(user["_id"])
    return user

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(user: User):
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email address already exists in the system.")
    
    user.hashed_password = auth.get_password_hash(user.hashed_password)
    user_dict = user.dict(by_alias=True)
    del user_dict["id"]
    users_collection.insert_one(user_dict)
    user.id = str(user_dict.get("_id"))
    return user

@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "User deleted successfully"}

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: str, updated_user: User):
    existing_user = users_collection.find_one({"email": updated_user.email})
    if existing_user and str(existing_user["_id"]) != user_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email address already in use.")
    
    updated_user_dict = updated_user.dict(by_alias=True)
    del updated_user_dict["id"]
    users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_user_dict})
    return updated_user

@router.post("/login", response_model=dict)
def login(email: str, password: str):
    user = users_collection.find_one({"email": email})
    if not user or not auth.verify_password(password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    access_token = auth.create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}



@router.post("/register", response_model=User)
def register(user_data: UserRegistration):
    if not user_data.company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company name must not be empty")

    # Vérifiez si la compagnie existe dans la base de données par son nom
    existing_company = companies_collection.find_one({"name": user_data.company})
    if not existing_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company does not exist")

    # Vérifiez si l'email est déjà utilisé
    existing_user = users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already in use")

    hashed_password = auth.get_password_hash(user_data.password.get_secret_value())
    new_user_dict = {
        "name": user_data.name,
        "email": user_data.email,
        "hashed_password": hashed_password,
        "company": user_data.company,  # Ici, nous stockons juste le nom de la compagnie
    }

    new_user_id = users_collection.insert_one(new_user_dict).inserted_id
    new_user_dict["_id"] = str(new_user_id)
    del new_user_dict["hashed_password"]  # Enlever le mot de passe haché de la sortie

    # Convertissez les champs nécessaires et retournez l'utilisateur
    new_user_dict["id"] = new_user_dict.pop("_id")  # Renommer "_id" en "id"
    return User(**new_user_dict)