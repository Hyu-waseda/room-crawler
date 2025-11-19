from dataclasses import dataclass


@dataclass
class Property:
    id: str
    title: str
    url: str
    address: str
    nearest_station: str
    walk_min: int
    rent_yen: int
    management_fee_yen: int
    area_m2: float
    floor: int
    age_year: int
    structure: str
