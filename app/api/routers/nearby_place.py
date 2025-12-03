from fastapi import APIRouter, Depends, HTTPException, status
from app.model import NearbyPlace
from app.database.database import get_session
from sqlmodel import Session
from app.service import nearby_place_crud
from typing import List

router = APIRouter()


@router.get("/nearby-places/", response_model=List[NearbyPlace], status_code=status.HTTP_200_OK)
def get_nearby_places(db: Session = Depends(get_session)):
    nearby_places = nearby_place_crud.get_many(db)
    return nearby_places


@router.get("/nearby-places/{nearby_place_id}", response_model=NearbyPlace, status_code=status.HTTP_200_OK)
def get_nearby_place(nearby_place_id: int, db: Session = Depends(get_session)):
    nearby_place = nearby_place_crud.get_one(db, id=nearby_place_id)
    if not nearby_place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nearby place not found",
        )
    return nearby_place
