from app.service.base import CRUDRepository
from app.model.user import User
from sqlmodel import Session
from fastapi import UploadFile, HTTPException
import os
import shutil
from typing import List
from pathlib import Path

AVATAR_DIR = "static/avatars"

class UserCrud(CRUDRepository):
    def __init__(self):
        super().__init__(model=User)

    def update_avatar(self, db: Session, user_id: int, file: UploadFile) -> User:

        user = self.get_one(db, user_id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        filename = f"{user.id}_{file.filename}"
        file_path = str(Path(AVATAR_DIR) / filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        user.avatar = file_path
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
user_crud = UserCrud()
