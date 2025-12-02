from fastapi import FastAPI
from sqlmodel import SQLModel
from app.api import (
    auth_router,
    user_router,
    province_router,
    district_router,
    ward_router,
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
    create_db_and_tables()
    init_db()
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
app.include_router(user_router, prefix="/api/v1/users", tags=["users🙍"])
app.include_router(province_router, prefix="/api/v1/provinces", tags=["provinces🗾"])
app.include_router(district_router, prefix="/api/v1/districts", tags=["districts🌁"])
app.include_router(ward_router, prefix="/api/v1/wards", tags=["wards🛣️"])    