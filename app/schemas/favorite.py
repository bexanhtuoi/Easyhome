from pydantic import BaseModel
from typing import Optional

class FavoriteCreateSchema(BaseModel):
    property_id: int
    # user_id will be taken from access token on server side

class FavoriteResponseSchema(BaseModel):
    user_id: int
    property_id: int
