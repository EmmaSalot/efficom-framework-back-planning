
# System libs imports
from typing import Annotated

# Libs imports
from fastapi import APIRouter, HTTPException, status, Depends

# Local imports
from internal.auth import get_decoded_token
from models.users import CreateUser, User

router= APIRouter()


# response_model_exclude_unset -> This remove the attributes that are not set in the response (= null or None)
@router.get("/users", response_model_exclude_unset=True)
async def getUsers(connected_user_email: Annotated[str, Depends(get_decoded_token)]) -> list[User]:
    """
    Endpoint to return all users
    """
    return users

@router.get("/users/{user_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str}})
async def getUser(user_id: int) -> User:
    """
    Endpoint to return a specific user based on id
    """
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.post("/users", status_code=status.HTTP_201_CREATED, responses={status.HTTP_409_CONFLICT: {"model": str}})
async def createUser(user: CreateUser) -> User:
    """
    Endpoint to create a new user and add it to the list of users
    """
    max_id = 0
    for existing_user in users:
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email address already exists in the system.")
        if existing_user["id"] > max_id:
            max_id = existing_user["id"]

    # we made the checks before for the email, so we can be sure that the email is unique
    # we raise errors in that case and this piece of code won't be executed
    user = user.dict()
    user['id'] = max_id + 1
    users.append(user)
    return user

@router.delete("/users/{user_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str}})
async def deleteUser(user_id: int) -> None:
    for index, user in enumerate(users):
        if user["id"] == user_id:
            users.pop(index)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.put("/users/{user_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str},
                                        status.HTTP_409_CONFLICT: {"model": str}})
async def updateUser(user_id: int, updated_user: CreateUser) -> None:
    user_index = None
    for index, user in enumerate(users):
        if user["email"] == updated_user.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email address already exists in the system.")
        if user["id"] == user_id:
            user_index = index
    
    if user_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    updated_user = updated_user.dict()
    updated_user["id"] = user_id
    users[user_index]= updated_user