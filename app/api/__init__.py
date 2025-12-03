from app.api.routers.auth import router as auth_router
from app.api.routers.user import router as user_router
from app.api.routers.province import router as province_router
from app.api.routers.district import router as district_router
from app.api.routers.ward import router as ward_router
from app.api.routers.category import router as category_router
from app.api.routers.amenities import router as amenities_router
from app.api.routers.object import router as object_router
from app.api.routers.nearby_place import router as nearby_place_router
from app.api.routers.review import router as review_router
from app.api.routers.favorite import router as favorite_router

__all__ = [
    "auth_router",
    "user_router",
    "province_router",
    "district_router",
    "ward_router",
    "category_router",
    "amenities_router",
    "object_router",
    "nearby_place_router",
    "review_router",
    "favorite_router",
]