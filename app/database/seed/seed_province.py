import requests
from sqlmodel import Session
from app.database.database import engine
from app.model import Province

API_URL = "https://provinces.open-api.vn/api/v1/"

def seed_provinces():
    print("Fetching province data...")

    response = requests.get(API_URL)
    if response.status_code != 200:
        print("Failed to fetch data")
        return

    provinces_data = response.json()

    with Session(engine) as session:
        for item in provinces_data:
            province_id = item["code"]
            province_name = item["name"]

            # Check existing
            exists = session.get(Province, province_id)
            if exists:
                continue

            province = Province(
                id=province_id,
                name=province_name
            )
            session.add(province)

        session.commit()
        print("Seed provinces completed!")
