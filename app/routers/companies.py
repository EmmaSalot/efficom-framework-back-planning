"""Endpoint to handle company operations"""

# System libs imports
from typing import Annotated
from internal import auth

# Libs imports
from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from auth import get_user_role_from_token
from fastapi.security import OAuth2PasswordBearer

# Local imports
from models.companies import CreateCompany, Company
from database import get_companies_collection

router= APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

companies_collection = get_companies_collection()


@router.get("/companies", response_model_exclude_unset=True)
async def getCompanies() -> list[Company]:
    """
    Endpoint to return all companies
    """
    return list(companies_collection.find({}, {"_id": 0}))


@router.get("/companies/{company_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str}})
async def getCompany(company_id: str) -> Company:
    """
    Endpoint to return a specific company based on id
    """
    company = companies_collection.find_one({"_id": ObjectId(company_id)}, {"_id": 0})
    if company:
        return company
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")


@router.post("/companies", status_code=status.HTTP_201_CREATED, responses={status.HTTP_409_CONFLICT: {"model": str}})
async def createCompany(company: CreateCompany, token: str = Depends(oauth2_scheme) ) -> Company:
    """
    Endpoint to create a new company and add it to the list of companies
    """
    user_role = get_user_role_from_token(token)
    
    if user_role != "sa":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only super admins can create companies")
    
    existing_company = companies_collection.find_one({"name": company.name})
    if existing_company:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Company name already exists in the system.")
    
    result = companies_collection.insert_one(company.dict())
    company_id = str(result.inserted_id)
    company = company.dict()
    company['id'] = company_id
    return company


@router.post("/companies/{company_id}/users/{user_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str},
                                        status.HTTP_409_CONFLICT: {"model": str}})
async def add_user_to_company(company_id: str, user_id: str) -> None:
    """
    Endpoint to add a user to a company
    """
    company = companies_collection.find_one({"_id": ObjectId(company_id)})
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    if user_id in company.get("users", []):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists in the company.")
    result = companies_collection.update_one(
        {"_id": ObjectId(company_id)},
        {"$push": {"users": user_id}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")


@router.delete("/companies/{company_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str}})
async def deleteCompany(company_id: str, token: str = Depends(oauth2_scheme)) -> None:
    """
    Endpoint to delete a company
    """
    user_role = get_user_role_from_token(token)
    
    if user_role != "sa":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only super admins can create companies")
    
    result = companies_collection.delete_one({"_id": ObjectId(company_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    if result.deleted_count > 0:
        return {"message": "Company deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")


@router.delete("/companies/{company_id}/users/{user_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str}})
async def delete_user_from_company(company_id: str, user_id: str) -> None:
    """
    Endpoint to delete a user from a company
    """
    company = companies_collection.find_one({"_id": ObjectId(company_id)})
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    if user_id not in company.get("users", []):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in the company.")

    result = companies_collection.update_one(
        {"_id": ObjectId(company_id)},
        {"$pull": {"users": user_id}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")


@router.post("/companies/{company_id}/activities/{activity_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str},
                                        status.HTTP_409_CONFLICT: {"model": str}})
async def add_activity_to_company(company_id: str, activity_id: str) -> None:
    """
    Endpoint to add an activity to a company
    """
    company = companies_collection.find_one({"_id": ObjectId(company_id)})
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    if activity_id in company.get("activities", []):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Activity already exists in the company.")

    result = companies_collection.update_one(
        {"_id": ObjectId(company_id)},
        {"$push": {"activities": activity_id}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")


@router.delete("/companies/{company_id}/activities/{activity_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str}})
async def delete_activity_from_company(company_id: str, activity_id: str) -> None:
    """
    Endpoint to delete an activity from a company
    """
    company = companies_collection.find_one({"_id": ObjectId(company_id)})
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    if activity_id not in company.get("activities", []):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found in the company.")

    result = companies_collection.update_one(
        {"_id": ObjectId(company_id)},
        {"$pull": {"activities": activity_id}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")


@router.put("/companies/{company_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str},
                                        status.HTTP_409_CONFLICT: {"model": str}})
async def updateCompany(company_id: str, updated_company: CreateCompany) -> None:
    """
    Endpoint to update a company
    """
    existing_company = companies_collection.find_one({"name": updated_company.name})
    if existing_company and existing_company["_id"] != ObjectId(company_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Company name already exists in the system.")
    
    result = companies_collection.update_one({"_id": ObjectId(company_id)}, {"$set": updated_company.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
