from app.model import PropertyImages
from app.service.base import CRUDRepository
from fastapi import UploadFile, HTTPException
from sqlmodel import Session
import os
import shutil
from pathlib import Path
from typing import List

PROPERTY_IMAGES_DIR = "static/property_images"

class PropertyImagesCrud(CRUDRepository):
    def __init__(self):
        super().__init__(model=PropertyImages)


    def upload_images(self, db: Session, property_id: int, files: List[UploadFile], is_thumbnail: bool = False) -> List[PropertyImages]:
        # Ensure directory exists
        Path(PROPERTY_IMAGES_DIR).mkdir(parents=True, exist_ok=True)

        current_count = len(self.get_many(db, property_id=property_id))
        if current_count + len(files) > 10:
            raise HTTPException(status_code=400, detail="Uploading these files would exceed the maximum of 10 images per property")

        created = []
        for file in files:
            filename = f"property_{property_id}_{file.filename}"
            file_path = str(Path(PROPERTY_IMAGES_DIR) / filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            image_obj = {
                "property_id": property_id,
                "image_url": file_path,
                "is_thumbnail": is_thumbnail,
            }
            created_obj = self.create(db, image_obj)
            created.append(created_obj)

        return created

    def replace_image(self, db: Session, image_id: int, file: UploadFile) -> PropertyImages:
        image = self.get_one(db, id=image_id)
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        # remove old file if exists
        if os.path.exists(image.image_url):
            try:
                os.remove(image.image_url)
            except Exception:
                pass

        # write new file
        filename = f"property_{image.property_id}_{file.filename}"
        file_path = str(Path(PROPERTY_IMAGES_DIR) / filename)
        Path(PROPERTY_IMAGES_DIR).mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # update db
        updated = self.update(db, db_obj=image, obj_in={"image_url": file_path})
        return updated
    
    def delete_image(self, db: Session, image_id: int) -> PropertyImages:
        image = self.get_one(db, id=image_id)
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Check if property will have 0 images after delete
        remaining_count = len(self.get_many(db, property_id=image.property_id)) - 1
        if remaining_count < 1:
            raise HTTPException(status_code=400, detail="Property must have at least 1 image")
        
        # Delete file from disk
        if os.path.exists(image.image_url):
            os.remove(image.image_url)
        
        return self.delete(db, image)

property_images_crud = PropertyImagesCrud()
