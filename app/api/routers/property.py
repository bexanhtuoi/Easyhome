from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database.database import get_session
from app.service.property import property_crud
from app.schemas.property import (
    PropertyCreateSchema,
    PropertyUpdateSchema
)
from app.model import Property
from app.api.dependencies import get_token, get_pagination_params
from typing import List

router = APIRouter()


@router.get("/properties/{property_id}", response_model=Property, status_code=status.HTTP_200_OK)
def get_property(
    property_id: int,
    db: Session = Depends(get_session)
):
    db_obj = property_crud.get_one(Property, id=property_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_obj


@router.get("/properties/", response_model=List[Property], status_code=status.HTTP_200_OK)
def get_properties(
    db: Session = Depends(get_session),
    pagination: tuple[int, int] = Depends(get_pagination_params)
):
    skip, limit = pagination
    properties = property_crud.get_many(db, skip=skip, limit=limit)
    return properties


@router.post("/properties/", response_model=Property, status_code=status.HTTP_201_CREATED)
def create_property(
    payload: PropertyCreateSchema,
    db: Session = Depends(get_session),
    access_token: str = Depends(get_token)
):

    payload.owner_id = int(access_token)

    db_obj = property_crud.create_property(db, payload)

    updated = property_crud.attach_relations(db, db_obj, payload)

    return updated


@router.patch("/properties/{property_id}", response_model=Property, status_code=status.HTTP_200_OK)
def update_property(
    property_id: int,
    payload: PropertyUpdateSchema,
    db: Session = Depends(get_session),
    access_token: str = Depends(get_token)
):
    db_obj = property_crud.get_one(db, id=property_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Property not found")

    if access_token != str(db_obj.owner_id):
        raise HTTPException(status_code=403, detail="Not authorized")

    updated = property_crud.update_property(db, db_obj, payload)
    return updated


@router.delete("/properties/{property_id}", response_model=Property, status_code=status.HTTP_200_OK)
def delete_property(
    property_id: int,
    db: Session = Depends(get_session),
    access_token: str = Depends(get_token)
):
    db_obj = property_crud.get_one(Property, id=property_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    
    if access_token != str(db_obj.owner_id):
        raise HTTPException(status_code=403, detail="Not authorized")

    deleted = property_crud.delete(db, db_obj=db_obj)
    return deleted
