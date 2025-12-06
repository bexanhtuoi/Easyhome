from sqlmodel import Session
from app.database.database import engine
from app.service import user_crud
from app.model import User
from app.model.user import RoleEnum, GenderEnum
from app.security import hash_password
from app.log import get_logger

log = get_logger(__name__)

def seed_users():
    with Session(engine) as session:

        user = user_crud.get_one(session, email="bexanhtuoi@gmail.com")

        if not user:
            user = User(
                full_name="Seed Admin",
                gender=GenderEnum.male,
                email="bexanhtuoi@gmail.com",
                password_hashed=hash_password("Admin@123"),
                role=RoleEnum.admin,
                is_verified=True,
            )
            session.add(user)
            session.commit()
            return

        user.role = RoleEnum.admin
        session.add(user)
        session.commit()
