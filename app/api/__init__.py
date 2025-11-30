from app.api.routers.auth import router as auth_router
from app.api.routers.user import router as user_router
from app.api.routers.province import router as province_router
from app.api.routers.district import router as district_router
from app.api.routers.ward import router as ward_router

__all__ = [
    "auth_router",
    "user_router",
    "province_router",
    "district_router",
    "ward_router",
]