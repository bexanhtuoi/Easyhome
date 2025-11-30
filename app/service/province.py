from app.model import Province
from app.service.base import CRUDRepository

class ProvinceCrud(CRUDRepository):
    def __init__(self):
        super().__init__(model=Province)

    
province_crud = ProvinceCrud()