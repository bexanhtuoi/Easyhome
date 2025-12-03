from fastapi import APIRouter, Depends, HTTPException, status
from app.model import Amenities
from app.database.database import get_session
from sqlmodel import Session
from app.service import amenities_crud
from typing import List

router = APIRouter()


@router.get("/amenities/", response_model=List[Amenities], status_code=status.HTTP_200_OK)
def get_amenities(db: Session = Depends(get_session)):
    amenities = amenities_crud.get_many(db)
    return amenities


@router.get("/amenities/{amenities_id}", response_model=Amenities, status_code=status.HTTP_200_OK)
def get_amenities_item(amenities_id: int, db: Session = Depends(get_session)):
    amenities = amenities_crud.get_one(db, id=amenities_id)
    if not amenities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Amenities not found",
        )
    return amenities
