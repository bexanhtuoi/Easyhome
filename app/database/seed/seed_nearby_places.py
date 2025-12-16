from sqlmodel import Session
from app.model import NearbyPlace
from app.log import get_logger
from app.database.database import engine

log = get_logger(__name__)
nearby_places_data = ['Bến xe Bus', 'Bệnh viện', 'Chợ', 'Công viên', 'Siêu thị', 'Trung tâm thể dục thể thao', 'Trường học']

def seed_nearby_places():
    log.info("Seeding nearby places data...")

    with Session(engine) as session:
        for place_name in nearby_places_data:
            # Check existing
            exists = session.query(NearbyPlace).filter(NearbyPlace.name == place_name).first()
            if exists:
                continue

            place = NearbyPlace(
                name=place_name
            )
            session.add(place)

        session.commit()
        log.info("Seed nearby places completed!")