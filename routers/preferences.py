from fastapi import APIRouter
from enum import Enum
from pydantic import BaseModel

router = APIRouter(
    prefix="/preferences",
    tags=["Hotel Preferences"]
)

# ------------------ ENUMS ------------------

class HotelType(str, Enum):
    resort = "Resort"
    hotel = "Hotel"
    boutique = "Boutique"
    luxury = "Luxury"

class RoomType(str, Enum):
    single = "Single"
    double = "Double"
    suite = "Suite"
    king = "King"


# ------------------ REQUEST MODEL ------------------

class PreferenceRequest(BaseModel):
    hotel_type: HotelType
    room_type: RoomType
    sea_view: bool
    stars: int


# ------------------ RESPONSE ------------------

@router.post("/recommend")
def recommend_hotel(preference: PreferenceRequest):

    # Basit recommendation logic (these are some fake data for testing.)
    if preference.hotel_type == HotelType.resort and preference.sea_view:
        return {
            "recommended_hotel": "Rotterdam Luxor Hotel"
        }

    elif preference.stars >= 5:
        return {
            "recommended_hotel": "Hotel Motopp 5 stars"
        }

    elif preference.room_type == RoomType.suite:
        return {
            "recommended_hotel": "Elite Suite Hotel, Schinnen"
        }

    else:
        return {
            "recommended_hotel": "Hotel California , such a lovely place.️"
        }