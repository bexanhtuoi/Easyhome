from app.database.seed import seed_users
from app.database.seed import seed_provinces
from app.database.seed import seed_districts
from app.database.seed import seed_wards

def init_db():
    # Seed initial data
    seed_users()
    seed_provinces()
    seed_districts()
    seed_wards()
