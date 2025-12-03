from app.model import Favorite
from app.service.base import CRUDRepository


class FavoriteCrud(CRUDRepository):
    def __init__(self):
        super().__init__(model=Favorite)


favorite_crud = FavoriteCrud()
