"""Endpoint to handle planning operations"""

# System libs imports
from typing import Annotated
from internal import auth

# Libs imports
from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from fastapi.security import OAuth2PasswordBearer
from auth import get_user_role_from_token


# Local imports
from models.plannings import CreatePlanning, Planning
from database import get_plannings_collection

router = APIRouter()
plannings_collection = get_plannings_collection()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.get("/plannings", response_model_exclude_unset=True)
async def get_plannings() -> list[Planning]:
    """
    Endpoint to return all plannings
    """
    return list(plannings_collection.find({}, {"_id": 0}))


@router.get("/plannings/{planning_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str}})
async def get_planning(planning_id: str) -> Planning:
    """
    Endpoint to return a specific planning based on id
    """
    planning = plannings_collection.find_one({"_id": ObjectId(planning_id)}, {"_id": 0})
    if planning:
        return planning
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planning not found")


@router.post("/plannings", status_code=status.HTTP_201_CREATED, responses={status.HTTP_409_CONFLICT: {"model": str}})
async def create_planning(planning: CreatePlanning,  token: str = Depends(oauth2_scheme)) -> Planning:
    """
    Endpoint to create a new planning and add it to the list of plannings
    """
    
    current_user_role = get_user_role_from_token(token)
    if current_user_role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create plannings")

    result = plannings_collection.insert_one(planning.dict())
    planning_id = str(result.inserted_id)
    planning = planning.dict()
    planning['id'] = planning_id
    return planning


@router.delete("/plannings/{planning_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str}})
async def delete_planning(planning_id: str, token: str = Depends(oauth2_scheme)) -> None:
    """
    Endpoint to delete a planning
    """
    
    current_user_role = get_user_role_from_token(token)
    if current_user_role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete plannings")

    result = plannings_collection.delete_one({"_id": ObjectId(planning_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planning not found")
    if result.deleted_count > 0:
        return {"message": "Planning deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planning not found")


@router.put("/plannings/{planning_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str}})
async def update_planning(planning_id: str, updated_planning: CreatePlanning) -> None:
    """
    Endpoint to update a planning
    """
    result = plannings_collection.update_one({"_id": ObjectId(planning_id)}, {"$set": updated_planning.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planning not found")


@router.post("/plannings/{planning_id}/activities/{activity_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str},
                                        status.HTTP_409_CONFLICT: {"model": str}})
async def add_activity_to_planning(planning_id: str, activity_id: str) -> None:
    """
    Endpoint to add an activity to a planning
    """
    planning = plannings_collection.find_one({"_id": ObjectId(planning_id)})
    if not planning:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planning not found")
    if activity_id in planning.get("activities", []):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Activity already exists in the planning.")

    result = plannings_collection.update_one(
        {"_id": ObjectId(planning_id)},
        {"$push": {"activities": activity_id}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planning not found")


@router.delete("/plannings/{planning_id}/activities/{activity_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str}})
async def delete_activity_from_planning(planning_id: str, activity_id: str) -> None:
    """
    Endpoint to delete an activity from a planning
    """
    planning = plannings_collection.find_one({"_id": ObjectId(planning_id)})
    if not planning:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planning not found")

    if activity_id not in planning.get("activities", []):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found in the planning.")

    result = plannings_collection.update_one(
        {"_id": ObjectId(planning_id)},
        {"$pull": {"activities": activity_id}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planning not found")
