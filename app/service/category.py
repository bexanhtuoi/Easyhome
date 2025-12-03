from app.model import Category
from app.service.base import CRUDRepository


class CategoryCrud(CRUDRepository):
    def __init__(self):
        super().__init__(model=Category)


category_crud = CategoryCrud()
