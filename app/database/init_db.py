from app.database.seed import seed_users
from app.database.seed import seed_provinces
from app.database.seed import seed_districts
from app.database.seed import seed_wards
from app.log import get_logger

log = get_logger(__name__)

def init_db():
    # Seed initial data
    log.info("Bắt đầu seeding data")
    seed_users()
    seed_provinces()
    seed_districts()
    seed_wards()
    log.info("Seeding hoàn tất!")
