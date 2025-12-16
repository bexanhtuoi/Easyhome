from app.model import Property, Amenities, Object, NearbyPlace
from app.service.base import CRUDRepository
from typing import List, Optional, Union, TypeVar
from sqlmodel import SQLModel, Session, select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from fastapi import HTTPException

ORMModel = TypeVar("ORMModel", bound=SQLModel)

class PropertyCrud(CRUDRepository):
    def __init__(self):
        super().__init__(model=Property)

    def create_property(self, db: Session, obj_in: BaseModel) -> ORMModel:
        field_exclude = {"amenities_id", "objects_id", "nearby_places_id"}

        db_obj = self._model(
            **obj_in.model_dump(exclude_unset=True, exclude=field_exclude)
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def attach_relations(self, db: Session, property: Property, data: BaseModel) -> ORMModel:

        # --- Amenities ---
        if data.amenities_id:
            amenities = db.exec(
                select(Amenities).where(Amenities.id.in_(data.amenities_id))
            ).all()

            if len(amenities) != len(data.amenities_id):
                raise HTTPException(status_code=400, detail="Invalid amenities_id")

            property.amenities = amenities

        # --- Objects ---
        if data.objects_id:
            objects = db.exec(
                select(Object).where(Object.id.in_(data.objects_id))
            ).all()

            if len(objects) != len(data.objects_id):
                raise HTTPException(status_code=400, detail="Invalid objects_id")

            property.objects = objects

        # --- Nearby places ---
        if data.nearby_places_id:
            nb_places = db.exec(
                select(NearbyPlace).where(NearbyPlace.id.in_(data.nearby_places_id))
            ).all()

            if len(nb_places) != len(data.nearby_places_id):
                raise HTTPException(status_code=400, detail="Invalid nearby_places_id")

            property.nearby_places = nb_places

        db.add(property)
        db.commit()
        db.refresh(property)

        return property

    
    def update_property(self, db: Session, db_obj: Property, obj_in: BaseModel):

        exclude_fields = {"amenities_id", "objects_id", "nearby_places_id"}

        update_data = obj_in.model_dump(exclude_unset=True, exclude=exclude_fields)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        self.attach_relations(db, db_obj, obj_in)

        return db_obj

    def get_one_with_relations(self, db: Session, id: int) -> Optional[Property]:
        stmt = select(self._model).where(self._model.id == id).options(
            selectinload(self._model.amenities),
            selectinload(self._model.objects),
            selectinload(self._model.nearby_places),
            selectinload(self._model.images),
        )
        return db.exec(stmt).first()

    def get_many_with_relations(self, db: Session, skip: int = 0, limit: int = 100) -> List[Property]:
        stmt = select(self._model).options(
            selectinload(self._model.amenities),
            selectinload(self._model.objects),
            selectinload(self._model.nearby_places),
            selectinload(self._model.images),
        ).offset(skip).limit(limit)
        return db.exec(stmt).all()


    
property_crud = PropertyCrud()