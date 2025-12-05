from fastapi import FastAPI
from sqlmodel import SQLModel
from app.api import (
    auth_router,
    google_auth_router,
    facebook_auth_router,
    user_router,
    province_router,
    district_router,
    ward_router,
    category_router,
    amenities_router,
    object_router,
    nearby_place_router,
    review_router,
    favorite_router,
    property_images_router
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.database.database import create_db_and_tables
from app.database.init_db import init_db

from contextlib import asynccontextmanager
import os
os.makedirs("static/avatars", exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    # create_db_and_tables() nên gỡ vì đã có alembic
    # init_db() seed dữ liệu
    print("Database ready!")
    yield
    # shutdown
    print("App shutdown")

app = FastAPI(
    lifespan=lifespan,
    title="EasyHome",
    description="API for EasyHome",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to the EasyHome API"}

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth🔐"])
app.include_router(google_auth_router, prefix="/api/v1/auth", tags=["google_auth🔐"])
app.include_router(facebook_auth_router, prefix="/api/v1/auth", tags=["facebook_auth🔐"])
app.include_router(user_router, prefix="/api/v1/users", tags=["users🙍"])
app.include_router(province_router, prefix="/api/v1/provinces", tags=["provinces🗾"])
app.include_router(district_router, prefix="/api/v1/districts", tags=["districts🌁"])
app.include_router(ward_router, prefix="/api/v1/wards", tags=["wards🛣️"])
app.include_router(category_router, prefix="/api/v1/categories", tags=["categories🏷️"])
app.include_router(amenities_router, prefix="/api/v1/amenities", tags=["amenities🛏️"])
app.include_router(object_router, prefix="/api/v1/objects", tags=["objects📦"])
app.include_router(nearby_place_router, prefix="/api/v1/nearby-places", tags=["nearby_places🗺️"])    
app.include_router(review_router, prefix="/api/v1/reviews", tags=["reviews⭐"])
app.include_router(favorite_router, prefix="/api/v1/favorites", tags=["favorites❤️"])
app.include_router(property_images_router, prefix="/api/v1/property-images", tags=["Images🖼️"])
