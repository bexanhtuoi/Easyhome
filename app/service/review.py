from app.model import Review
from app.service.base import CRUDRepository


class ReviewCrud(CRUDRepository):
    def __init__(self):
        super().__init__(model=Review)


review_crud = ReviewCrud()
