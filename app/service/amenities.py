from app.model import Amenities
from app.service.base import CRUDRepository


class AmenitiesCrud(CRUDRepository):
    def __init__(self):
        super().__init__(model=Amenities)


amenities_crud = AmenitiesCrud()
