from fastapi import APIRouter, Depends, HTTPException, status
from app.model import Object
from app.database.database import get_session
from sqlmodel import Session
from app.service import object_crud
from typing import List

router = APIRouter()


@router.get("/objects/", response_model=List[Object], status_code=status.HTTP_200_OK)
def get_objects(db: Session = Depends(get_session)):
    objects = object_crud.get_many(db)
    return objects


@router.get("/objects/{object_id}", response_model=Object, status_code=status.HTTP_200_OK)
def get_object(object_id: int, db: Session = Depends(get_session)):
    obj = object_crud.get_one(db, id=object_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Object not found",
        )
    return obj
