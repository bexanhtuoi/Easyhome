from fastapi import APIRouter, Depends, HTTPException, status
from app.model import User, Ward
from app.database.database import get_session
from sqlmodel import Session

from app.service import ward_crud
from typing import List

router = APIRouter()

@router.get("/wards/", response_model=List[Ward], status_code=status.HTTP_200_OK)
def get_wards(db: Session = Depends(get_session)):
    wards = ward_crud.get_many(db)
    return wards

@router.get("/wards/{ward_id}", response_model=Ward, status_code=status.HTTP_200_OK)
def get_ward(ward_id: int, db: Session = Depends(get_session)):
    ward = ward_crud.get_one(db, id=ward_id)
    if not ward:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ward not found",
        )
    return ward

@router.get("/district/{district_id}/wards/", response_model=List[Ward], status_code=status.HTTP_200_OK)
def get_wards_by_district(district_id: int, db: Session = Depends(get_session)):
    wards = ward_crud.get_many(db, district_id=district_id)
    return wards

    