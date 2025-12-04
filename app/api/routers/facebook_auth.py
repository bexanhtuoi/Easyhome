from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from fastapi.responses import JSONResponse, RedirectResponse
from datetime import timedelta
import httpx

from app.database.database import get_session
from app.service import user_crud
from app.core.config import settings
from app.security import create_access_token

router = APIRouter()

FB_AUTH_URL = "https://www.facebook.com/v18.0/dialog/oauth"
FB_TOKEN_URL = "https://graph.facebook.com/v18.0/oauth/access_token"
FB_ME_URL = "https://graph.facebook.com/me"

@router.get("/facebook/login")
def facebook_login():
    params = (
        f"?client_id={settings.facebook_client_id}"
        f"&redirect_uri={settings.facebook_redirect_uri}"
        f"&scope=email,public_profile"
        f"&response_type=code"
    )
    fb_url = FB_AUTH_URL + params
    return RedirectResponse(fb_url)


@router.get("/facebook/callback")
async def facebook_callback(code: str, db: Session = Depends(get_session)):
    async with httpx.AsyncClient() as client:
        token_resp = await client.get(
            FB_TOKEN_URL,
            params={
                "client_id": settings.facebook_client_id,
                "client_secret": settings.facebook_client_secret,
                "redirect_uri": settings.facebook_redirect_uri,
                "code": code,
            },
        )

    if token_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Facebook token exchange failed")

    tokens = token_resp.json()
    access_token = tokens.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="No access token returned by Facebook")

    async with httpx.AsyncClient() as client:
        userinfo_resp = await client.get(
            FB_ME_URL,
            params={
                "fields": "id,name,email,picture",
                "access_token": access_token,
            },
        )

    if userinfo_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get Facebook user info")

    info = userinfo_resp.json()
    print(info)
    email = info.get("email")
    name = info.get("name")
    picture = info.get("picture", {}).get("data", {}).get("url")

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Facebook account does not provide email. Cannot login.",
        )

    db_user = user_crud.get_one(db, email=email)

    if not db_user:
        obj_in_data = {
            "email": email,
            "full_name": name,
            "avatar": picture,
            "password_hashed": None,
        }
        db_user = user_crud.create(db, obj_in=obj_in_data)

    token_expires = timedelta(minutes=settings.access_token_expires_minutes)

    jwt_token = create_access_token(
        data=db_user.id,
        expires_delta=token_expires
    )

    response = JSONResponse(content={"message": "Login with Facebook successful"})
    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        secure=False,
        samesite="lax",
    )

    return response
