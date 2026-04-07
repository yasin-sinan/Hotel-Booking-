from pydantic import BaseModel, Field

class HotelRequest(BaseModel):
    name: str
    hotel_type: str
    room_type: str
    sea_view: bool
    stars: int = Field(ge=1, le=5)
    price_per_night: int = Field(ge=0)

class HotelResponse(BaseModel):
    id: int
    name: str
    hotel_type: str
    room_type: str
    sea_view: bool
    stars: int
    price_per_night: int

    model_config = {"from_attributes": True}