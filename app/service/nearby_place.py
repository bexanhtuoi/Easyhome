from app.model import NearbyPlace
from app.service.base import CRUDRepository


class NearbyPlaceCrud(CRUDRepository):
    def __init__(self):
        super().__init__(model=NearbyPlace)


nearby_place_crud = NearbyPlaceCrud()
