from app.model import Object
from app.service.base import CRUDRepository


class ObjectCrud(CRUDRepository):
    def __init__(self):
        super().__init__(model=Object)


object_crud = ObjectCrud()
