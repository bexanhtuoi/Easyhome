from sqlmodel import Session
from app.model import Category
from app.log import get_logger
from app.database.database import engine

log = get_logger(__name__)

categories = ['Căn hộ', 'Ký túc xá', 'Nhà nguyên căn', 'Nhà trọ, phòng trọ - Chủ quản', 'Nhà trọ, phòng trọ - Tự quản']

def seed_categories():
    log.info("Seeding categories data...")

    with Session(engine) as session:
        for category_name in categories:
            # Check existing
            exists = session.query(Category).filter(Category.name == category_name).first()
            if exists:
                continue

            category = Category(
                name=category_name
            )
            session.add(category)

        session.commit()
        log.info("Seed categories completed!")