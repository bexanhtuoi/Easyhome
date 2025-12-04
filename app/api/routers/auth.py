from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database.database import get_session
from app.model import User
from app.service import user_crud
from app.schemas.user import UserCreateSchema, Token
from app.security import hash_password, verify_password
from app.core.config import settings
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.security import create_access_token

router = APIRouter()

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreateSchema, db: Session = Depends(get_session)):
    db_user = user_crud.get_one(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    obj_in_data = user_in.model_dump()

    obj_in_data["password_hashed"] = hash_password(obj_in_data.pop("password"))

    new_user = user_crud.create(db, obj_in=obj_in_data)

    return new_user




@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login(db: Session = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = user_crud.get_one(db, email=form_data.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    if not verify_password(form_data.password, db_user.password_hashed):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    access_token_expires = timedelta(minutes=settings.access_token_expires_minutes)
    access_token = create_access_token(
        data=db_user.id,
        expires_delta=access_token_expires
    )

    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(key="access_token",
                         value=access_token,
                          httponly=True,
                          secure=False,
                          samesite="lax")

    return response


@router.post("/logout", response_model=dict, status_code=status.HTTP_200_OK)
def logout():
    response = JSONResponse(content={"message": "Logout successful"})
    response.delete_cookie(key="access_token")
    return response