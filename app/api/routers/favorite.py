from fastapi import APIRouter, Depends, HTTPException, status
from app.model import Favorite
from app.database.database import get_session
from sqlmodel import Session
from app.service import favorite_crud
from typing import List
from app.api.dependencies import get_token
from app.schemas.favorite import FavoriteCreateSchema

router = APIRouter()


@router.get("/", response_model=List[Favorite], status_code=status.HTTP_200_OK)
def get_favorites(db: Session = Depends(get_session)):
    return favorite_crud.get_many(db)


@router.get("/user/{user_id}", response_model=List[Favorite], status_code=status.HTTP_200_OK)
def get_favorites_by_user(user_id: int, db: Session = Depends(get_session)):
    return favorite_crud.get_many(db, user_id=user_id)


@router.get("/property/{property_id}", response_model=List[Favorite], status_code=status.HTTP_200_OK)
def get_favorites_by_property(property_id: int, db: Session = Depends(get_session)):
    return favorite_crud.get_many(db, property_id=property_id)


@router.get("/{user_id}/{property_id}", response_model=Favorite, status_code=status.HTTP_200_OK)
def get_favorite(user_id: int, property_id: int, db: Session = Depends(get_session)):
    fav = favorite_crud.get_one(db, user_id=user_id, property_id=property_id)
    if not fav:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found")
    return fav


@router.post("/", response_model=Favorite, status_code=status.HTTP_201_CREATED)
def create_favorite(
    favorite_in: FavoriteCreateSchema,
    db: Session = Depends(get_session),
    access_token: str = Depends(get_token),
):
    try:
        user_id = int(access_token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token user id")

    existing = favorite_crud.get_one(db, user_id=user_id, property_id=favorite_in.property_id)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Favorite already exists")

    obj = {"user_id": user_id, "property_id": favorite_in.property_id}
    created = favorite_crud.create(db, obj)
    return created


@router.delete("/{user_id}/{property_id}", response_model=Favorite, status_code=status.HTTP_200_OK)
def delete_favorite(user_id: int, property_id: int, db: Session = Depends(get_session), access_token: str = Depends(get_token)):
    
    if int(access_token) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this favorite")

    fav = favorite_crud.get_one(db, user_id=user_id, property_id=property_id)
    if not fav:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found")
    deleted = favorite_crud.delete(db, fav)
    return deleted
