from sqlmodel import Session
from app.model import Object
from app.log import get_logger
from app.database.database import engine

log = get_logger(__name__)
objects_data = ['Cặp đôi', 'Gia đình', 'Đi học', 'Đi làm']

def seed_objects():
    log.info("Seeding objects data...")

    with Session(engine) as session:
        for object_name in objects_data:
            # Check existing
            exists = session.query(Object).filter(Object.name == object_name).first()
            if exists:
                continue

            obj = Object(
                name=object_name
            )
            session.add(obj)

        session.commit()
        log.info("Seed objects completed!")