import requests
from sqlmodel import Session
from app.database.database import engine
from app.model import Province, Ward
from app.log import get_logger

API_URL = "https://provinces.open-api.vn/api/v1/p/{code}?depth=3"

log = get_logger(__name__)

def seed_wards():
    with Session(engine) as session:

        provinces = session.query(Province).all()
        log.info(f"Found {len(provinces)} provinces. Seeding wards...")

        for province in provinces:
            log.info(f"Fetching ward data for province {province.name} ({province.id})")

            url = API_URL.format(code=province.id)
            response = requests.get(url)

            if response.status_code != 200:
                log.error(f"Failed to fetch wards for province {province.id}")
                continue

            province_data = response.json()
            districts = province_data.get("districts", [])

            for district in districts:
                district_id = district["code"]
                ward_list = district.get("wards", [])

                for item in ward_list:
                    ward_id = item["code"]
                    ward_name = item["name"]
                    district_code = item["district_code"]

                    # Check nếu ward đã tồn tại
                    exists = session.get(Ward, ward_id)
                    if exists:
                        continue

                    ward = Ward(
                        id=ward_id,
                        name=ward_name,
                        district_id=district_code
                    )
                    session.add(ward)

        session.commit()

    log.info("Seed wards completed!")
