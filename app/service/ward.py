from app.model import Ward
from app.service.base import CRUDRepository

class WardCrud(CRUDRepository):
    def __init__(self):
        super().__init__(model=Ward)
        
ward_crud = WardCrud()