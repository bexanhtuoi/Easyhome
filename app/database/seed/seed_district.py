import requests
from sqlmodel import Session
from app.database.database import engine
from app.model import Province, District

API_URL = "https://provinces.open-api.vn/api/v1/p/{code}?depth=2"


def seed_districts():
    with Session(engine) as session:

        # Lấy toàn bộ province trong DB
        provinces = session.query(Province).all()

        print(f"Found {len(provinces)} provinces. Seeding districts...")

        for province in provinces:
            print(f"Fetching districts for province {province.name} ({province.id})")

            url = API_URL.format(code=province.id)
            response = requests.get(url)

            if response.status_code != 200:
                print(f"Failed to fetch districts for province {province.id}")
                continue

            data = response.json()
            district_list = data.get("districts", [])

            for item in district_list:
                district_id = item["code"]
                district_name = item["name"]
                province_id = item["province_code"]

                # Check nếu district đã tồn tại
                exists = session.get(District, district_id)
                if exists:
                    continue

                district = District(
                    id=district_id,
                    name=district_name,
                    province_id=province_id,
                )
                session.add(district)

        session.commit()

    print("Seed districts completed!")
