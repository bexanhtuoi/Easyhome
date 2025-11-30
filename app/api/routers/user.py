from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database.database import get_session
from app.model import User, Province, District, Ward
from app.service import user_crud
from app.schemas.user import UserCreateSchema, UserUpdateSchema, Token
from app.api.dependencies import get_pagination_params, get_token
from app.security import hash_password
from app.core.config import settings
from datetime import datetime, timedelta
from typing import List
from fastapi import UploadFile, File


router = APIRouter()

@router.get("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def get_user(user_id: str, db: Session = Depends(get_session)):
    db_user = user_crud.get_one(db, id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return db_user


@router.get("/users/", response_model=List[User], status_code=status.HTTP_200_OK)
def get_users(
    db: Session = Depends(get_session),
    pagination: tuple[int, int] = Depends(get_pagination_params)
):
    skip, limit = pagination
    users = user_crud.get_many(db, skip=skip, limit=limit)
    return users

@router.get("/users/email/{email}", response_model=User, status_code=status.HTTP_200_OK)
def get_user_by_email(email: str, db: Session = Depends(get_session)):
    db_user = user_crud.get_one(db, email=email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return db_user

@router.get("/users/role/{role}", response_model=List[User], status_code=status.HTTP_200_OK)
def get_users_by_role(role: str, db: Session = Depends(get_session)):
    users = user_crud.get_many(db, role=role)
    return users

@router.patch("/users/{user_id}/avatar", response_model=User, status_code=status.HTTP_200_OK)
def upload_avatar(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_session),
    access_token: str = Depends(get_token)
):

    if str(user_id) != access_token:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = user_crud.update_avatar(db=db, user_id=user_id, file=file)
    
    return user

@router.patch("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def update_user(
    user_id: str,
    user_in: UserUpdateSchema,   
    db: Session = Depends(get_session),
    access_token: str = Depends(get_token)
):
    db_user = user_crud.get_one(db, id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if access_token != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user",
        )

    obj_in_data = user_in.model_dump(exclude_unset=True)

    if "password" in obj_in_data:
        obj_in_data["password_hashed"] = hash_password(obj_in_data.pop("password"))
        

    obj_in_data["update_at"] = datetime.utcnow()
    updated_user = user_crud.update(db, db_obj=db_user, obj_in=obj_in_data)
    return updated_user

@router.delete("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def delete_user(
    user_id: str,
    db: Session = Depends(get_session),
    access_token: str = Depends(get_token)
):
    db_user = user_crud.get_one(db, id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if access_token != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user",
        )

    deleted_user = user_crud.delete(db, db_obj=db_user)
    return deleted_user