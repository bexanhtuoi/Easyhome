from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from app.model import PropertyImages, Property
from app.database.database import get_session
from sqlmodel import Session
from app.service import property_images_crud, property_crud
from typing import List
from app.api.dependencies import get_token

router = APIRouter()


@router.get("/", response_model=List[PropertyImages], status_code=status.HTTP_200_OK)
def get_all_property_images(db: Session = Depends(get_session)):
    return property_images_crud.get_many(db)


@router.get("/property/{property_id}", response_model=List[PropertyImages], status_code=status.HTTP_200_OK)
def get_images_by_property(property_id: int, db: Session = Depends(get_session)):
    images = property_images_crud.get_many(db, property_id=property_id)
    if not images:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No images found for this property")
    return images


@router.get("/{image_id}", response_model=PropertyImages, status_code=status.HTTP_200_OK)
def get_property_image(image_id: int, db: Session = Depends(get_session)):
    image = property_images_crud.get_one(db, id=image_id)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return image


@router.post("/property/{property_id}", response_model=List[PropertyImages], status_code=status.HTTP_201_CREATED)
def upload_property_image(
    property_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_session),
    access_token: str = Depends(get_token),
    is_thumbnail: bool = False
):
    # Check if property exists and user owns it (use property_crud)
    property_obj = property_crud.get_one(db, id=property_id)
    if not property_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")

    # get_token already validates and returns the subject (user id as string)
    if access_token != str(property_obj.owner_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to upload images for this property")
    
    # files validation: at least 1, at most 10 by combined count enforced in service
    if not files or len(files) < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one file must be uploaded")

    uploaded = property_images_crud.upload_images(db, property_id, files, is_thumbnail)
    return uploaded


@router.patch("/{image_id}", response_model=PropertyImages, status_code=status.HTTP_200_OK)
def replace_property_image(
    image_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_session),
    access_token: str = Depends(get_token),
):
    image = property_images_crud.get_one(db, id=image_id)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    # check owner using property_crud
    property_obj = property_crud.get_one(db, id=image.property_id)
    if not property_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")

    if access_token != str(property_obj.owner_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update images for this property")

    updated = property_images_crud.replace_image(db, image_id, file)
    return updated


@router.delete("/{image_id}", response_model=PropertyImages, status_code=status.HTTP_200_OK)
def delete_property_image(
    image_id: int,
    db: Session = Depends(get_session),
    access_token: str = Depends(get_token)
):
    image = property_images_crud.get_one(db, id=image_id)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    
    # Fetch property to check ownership using property_crud
    property_obj = property_crud.get_one(db, id=image.property_id)

    if not property_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")

    if access_token != str(property_obj.owner_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete images for this property")
    
    deleted = property_images_crud.delete_image(db, image_id)
    return deleted
