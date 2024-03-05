
# System libs imports
from typing import Annotated

# Libs imports
from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId 

# Local imports
from internal.auth import get_decoded_token
from models.users import CreateUser, User
from database import get_users_collection

router= APIRouter()
users_collection = get_users_collection()

@router.get("/users", response_model_exclude_unset=True)
async def getUsers(connected_user_email: Annotated[str, Depends(get_decoded_token)]) -> list[User]:
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