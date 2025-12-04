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
import httpx

TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

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


@router.get("/google/login")
def google_login():
    params = (
        f"?client_id={settings.google_client_id}"
        f"&response_type=code"
        f"&redirect_uri={settings.google_redirect_uri}"
        f"&scope=openid%20email%20profile"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    print(f"?client_id={settings.google_client_id}")
    print(f"&redirect_uri={settings.google_redirect_uri}")
    google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth" + params
    return RedirectResponse(google_auth_url)



@router.get("/google/callback")
async def google_callback(code: str, db: Session = Depends(get_session)):
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            TOKEN_URL,
            data={
                "code": code,
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uri": settings.google_redirect_uri,
                "grant_type": "authorization_code",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    if token_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Google token exchange failed")

    tokens = token_resp.json()
    access_token = tokens.get("access_token")

    async with httpx.AsyncClient() as client:
        userinfo_resp = await client.get(
            USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )

    if userinfo_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get user info")

    info = userinfo_resp.json()

    email = info["email"]
    name = info.get("name")
    picture = info.get("picture")

    db_user = user_crud.get_one(db, email=email)

    if not db_user:
        obj_in_data = {
            "email": email,
            "full_name": name,
            "avatar": picture,
            "password_hashed": None
        }
        db_user = user_crud.create(db, obj_in=obj_in_data)

    token_expires = timedelta(
        minutes=settings.access_token_expires_minutes
    )

    jwt_token = create_access_token(
        data=db_user.id,
        expires_delta=token_expires
    )

    response = JSONResponse(content={"message": "Login with Google successful"})
    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        secure=False,
        samesite="lax",
    )

    return response


@router.post("/logout", response_model=dict, status_code=status.HTTP_200_OK)
def logout():
    response = JSONResponse(content={"message": "Logout successful"})
    response.delete_cookie(key="access_token")
    return response