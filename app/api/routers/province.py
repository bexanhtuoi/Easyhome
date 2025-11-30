from fastapi import APIRouter, Depends, HTTPException, status
from app.model import User, Province
from app.database.database import get_session
from sqlmodel import Session

from app.service import province_crud
from typing import List

router = APIRouter()

@router.get("/provinces/", response_model=List[Province], status_code=status.HTTP_200_OK)
def get_provinces(db: Session = Depends(get_session)):
    provinces = province_crud.get_many(db)
    return provinces

@router.get("/provinces/{province_id}", response_model=Province, status_code=status.HTTP_200_OK)
def get_province(province_id: int, db: Session = Depends(get_session)):
    province = province_crud.get_one(db, id=province_id)
    if not province:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Province not found",
        )
    return province

