# System libs imports
from typing import Annotated

# Libs imports
from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId

# Local imports
from models.activities import CreateActivity, Activity
from database import get_activites_collection


router= APIRouter()

companies_collection = get_activites_collection()

# Get all activities
@router.get("/activities", response_model_exclude_unset=True)
async def getAll(query) -> list[Activity]:
    
    return await companies_collection.find(query)


@router.get("/activities/{activity_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str}})
async def getActivity(activity_id: str) -> Activity:
    activity = companies_collection.find_one({"_id": ObjectId(activity_id)}, {"_id": 0})
    if activity:
        return activity
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")

@router.post("/activities", status_code=status.HTTP_201_CREATED, responses={status.HTTP_409_CONFLICT: {"model": str}})
async def createActivity(activity: CreateActivity) -> Activity:
    existing_activity = companies_collection.find_one({"name": activity.name})
    if existing_activity:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Activity name already exists in the system.")
    
    result = companies_collection.insert_one(activity.dict())
    activity_id = str(result.inserted_id)
    activity = activity.dict()
    activity['id'] = activity_id
    return activity

@router.delete("/activities/{activity_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str}})
async def deleteActivity(activity_id: str) -> None:
    result = companies_collection.delete_one({"_id": ObjectId(activity_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
    