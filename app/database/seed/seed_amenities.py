from sqlmodel import Session
from app.model import Amenities
from app.log import get_logger
from app.database.database import engine

amenities_data = ['Ban công/sân thượng', 'Bãi để xe riêng', 'Bình nóng lạnh', 'Camera an ninh', 'Giường nệm', 'Gác lửng', 'Hồ bơi', 'Kệ bếp', 'Máy giặt', 'Phòng tắm', 'Sân vườn', 'Thang máy', 'Tivi', 'Tủ lạnh', 'Tủ áo quần', 'Vệ sinh trong', 'Wifi', 'Điều hòa']
log = get_logger(__name__)

def seed_amenities():
    log.info("Seeding amenities data...")

    with Session(engine) as session:
        for amenity_name in amenities_data:
            # Check existing
            exists = session.query(Amenities).filter(Amenities.name == amenity_name).first()
            if exists:
                continue

            amenity = Amenities(
                name=amenity_name
            )
            session.add(amenity)

        session.commit()
        log.info("Seed amenities completed!")
