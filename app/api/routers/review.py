from fastapi import APIRouter, Depends, HTTPException, status
from app.model import Review
from app.database.database import get_session
from sqlmodel import Session
from app.service import review_crud
from typing import List
from app.api.dependencies import get_token, get_pagination_params
from app.schemas.review import ReviewCreateSchema, ReviewUpdateSchema
from datetime import datetime

router = APIRouter()


@router.get("/", response_model=List[Review], status_code=status.HTTP_200_OK)
def get_reviews(
    db: Session = Depends(get_session),
    pagination: tuple[int, int] = Depends(get_pagination_params)):

    skip, limit = pagination
    return review_crud.get_many(db, skip=skip, limit=limit)


@router.get("/{review_id}", response_model=Review, status_code=status.HTTP_200_OK)
def get_review(review_id: int, db: Session = Depends(get_session)):
    review = review_crud.get_one(db, id=review_id)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return review


@router.get("/property/{property_id}", response_model=List[Review], status_code=status.HTTP_200_OK)
def get_reviews_by_property(property_id: int, db: Session = Depends(get_session)):
    return review_crud.get_many(db, property_id=property_id)


@router.get("/user/{user_id}", response_model=List[Review], status_code=status.HTTP_200_OK)
def get_reviews_by_user(user_id: int, db: Session = Depends(get_session)):
    return review_crud.get_many(db, user_id=user_id)


@router.post("/", response_model=Review, status_code=status.HTTP_201_CREATED)
def create_review(
    review_in: ReviewCreateSchema,
    db: Session = Depends(get_session),
    access_token: str = Depends(get_token),
):
    review_in.user_id = int(access_token)

    created = review_crud.create(db, review_in)
    return created


@router.patch("/{review_id}", response_model=Review, status_code=status.HTTP_200_OK)
def update_review(
    review_id: int,
    review_in: ReviewUpdateSchema,
    db: Session = Depends(get_session),
    access_token: str = Depends(get_token),
):
    review = review_crud.get_one(db, id=review_id)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    if access_token != str(review.user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this review")

    obj_in_data = review_in.model_dump(exclude_unset=True)
    obj_in_data["update_at"] = datetime.utcnow()
    updated = review_crud.update(db, db_obj=review, obj_in=obj_in_data)
    return updated


@router.delete("/{review_id}", response_model=Review, status_code=status.HTTP_200_OK)
def delete_review(review_id: int, db: Session = Depends(get_session), access_token: str = Depends(get_token)):
    review = review_crud.get_one(db, id=review_id)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")


    if access_token != str(review.user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this review")

    deleted = review_crud.delete(db, review)
    return deleted
