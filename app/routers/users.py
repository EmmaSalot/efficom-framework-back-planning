
# System libs imports
from typing import Annotated, List

# Libs imports
from fastapi import APIRouter, HTTPException, status, Depends, Body
from bson import ObjectId 
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status
from internal import auth

# Local imports
from models.users import CreateUser, User, UserInDB 
from datetime import timedelta
from database import get_users_collection

router= APIRouter()
users_collection = get_users_collection()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/users", response_model_exclude_unset=True)
async def getUsers() -> list[User]:
    """
    Endpoint to return all users
    """
    return list(users_collection.find({}, {"_id": 0}))

@router.get("/users/{user_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str}})
async def getUser(user_id: str) -> User:
    """
    Endpoint to return a specific user based on id
    """
    user = users_collection.find_one({"_id": ObjectId(user_id)}, {"_id": 0})
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.post("/users", status_code=status.HTTP_201_CREATED, responses={status.HTTP_409_CONFLICT: {"model": str}})
async def createUser(user: CreateUser) -> User:
    """
    Endpoint to create a new user and add it to the list of users
    """
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email address already exists in the system.")
    
    result = users_collection.insert_one(user.dict())
    user_id = str(result.inserted_id)
    user = user.dict()
    user['id'] = user_id
    return user

@router.delete("/users/{user_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str}})
async def deleteUser(user_id: str) -> None:
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.put("/users/{user_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str},
                                        status.HTTP_409_CONFLICT: {"model": str}})
async def updateUser(user_id: str, updated_user: CreateUser) -> None:
    existing_user = users_collection.find_one({"email": updated_user.email})
    if existing_user and existing_user["_id"] != ObjectId(user_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email address already exists in the system.")
    
    result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_user.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.post("/users/register", response_model=User)
async def register(user: CreateUser):
    db = get_users_collection()
    existing_user = db.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password = auth.get_password_hash(user.password)
    new_user = UserInDB(**user.dict(), hashed_password=hashed_password)
    result = db.insert_one(new_user.dict(by_alias=True))
    return new_user

@router.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_users_collection()
    user = auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}