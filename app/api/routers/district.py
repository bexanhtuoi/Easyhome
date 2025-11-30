from fastapi import APIRouter, Depends, HTTPException, status
from app.model import User, District
from app.database.database import get_session
from sqlmodel import Session

from app.service import district_crud

from typing import List

router = APIRouter()

@router.get("/districts/", response_model=List[District], status_code=status.HTTP_200_OK)
def get_districts(db: Session = Depends(get_session)):
    districts = district_crud.get_many(db)
    return districts

@router.get("/districts/{district_id}", response_model=District, status_code=status.HTTP_200_OK)
def get_district(district_id: int, db: Session = Depends(get_session)):
    district = district_crud.get_one(db, id=district_id)
    if not district:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="District not found",
        )
    return district

@router.get("/province/{province_id}/districts/", response_model=List[District], status_code=status.HTTP_200_OK)
def get_districts_by_province(province_id: int, db: Session = Depends(get_session)):
    districts = district_crud.get_many(db, province_id=province_id)
    return districts