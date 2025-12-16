from app.database.seed import seed_users
from app.database.seed import seed_provinces
from app.database.seed import seed_districts
from app.database.seed import seed_wards
from app.database.seed import seed_nearby_places
from app.database.seed import seed_categories
from app.database.seed import seed_amenities
from app.database.seed import seed_objects
from app.log import get_logger

log = get_logger(__name__)

def init_db():
    # Seed initial data
    log.info("Bắt đầu seeding data")
    seed_users()
    seed_provinces()
    seed_districts()
    seed_wards()
    seed_nearby_places()
    seed_categories()
    seed_amenities()
    seed_objects()
    
    log.info("Seeding hoàn tất!")
