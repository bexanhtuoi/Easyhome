from app.model import District
from app.service.base import CRUDRepository

class DistrictCrud(CRUDRepository):
    def __init__(self):
        super().__init__(model=District)

district_crud = DistrictCrud()