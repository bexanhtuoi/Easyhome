from fastapi import APIRouter, Depends, HTTPException, status
from app.model import Category
from app.database.database import get_session
from sqlmodel import Session
from app.service import category_crud
from typing import List

router = APIRouter()


@router.get("/categories/", response_model=List[Category], status_code=status.HTTP_200_OK)
def get_categories(db: Session = Depends(get_session)):
    categories = category_crud.get_many(db)
    return categories


@router.get("/categories/{category_id}", response_model=Category, status_code=status.HTTP_200_OK)
def get_category(category_id: int, db: Session = Depends(get_session)):
    category = category_crud.get_one(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category
