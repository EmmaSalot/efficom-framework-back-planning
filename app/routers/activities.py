"""Endpoint to handle activity operations"""

# System libs imports
from typing import Annotated

# Libs imports
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

# Local imports
from models.activities import CreateActivity, Activity
from database import get_activities_collection

router = APIRouter()
activities_collection = get_activities_collection()


@router.get("/activities", response_model_exclude_unset=True)
async def get_activities() -> list[Activity]:
    """
    Endpoint to return all activities
    """
    return list(activities_collection.find({}, {"_id": 0}))


@router.get("/activities/{activity_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str}})
async def get_activity(activity_id: str) -> Activity:
    """
    Endpoint to return a specific activity based on id
    """
    activity = activities_collection.find_one({"_id": ObjectId(activity_id)}, {"_id": 0})
    if activity:
        return activity
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")


@router.post("/activities", status_code=status.HTTP_201_CREATED)
async def create_activity(activity: CreateActivity) -> Activity:
    """
    Endpoint to create a new activity and add it to the list of activities
    """
    result = activities_collection.insert_one(activity.dict())
    activity_id = str(result.inserted_id)
    activity = activity.dict()
    activity['id'] = activity_id
    return activity


@router.delete("/activities/{activity_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str}})
async def delete_activity(activity_id: str) -> None:
    """
    Endpoint to delete an activity
    """
    result = activities_collection.delete_one({"_id": ObjectId(activity_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
    if result.deleted_count > 0:
        return {"message": "Activity deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")


@router.put("/activities/{activity_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str}})
async def update_activity(activity_id: str, updated_activity: CreateActivity) -> None:
    """
    Endpoint to update an activity
    """
    result = activities_collection.update_one({"_id": ObjectId(activity_id)}, {"$set": updated_activity.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
