from pydantic import BaseModel
from typing import Optional
from datetime import date

class BookingModel(BaseModel):
    user_id: int
    hotel_name: str
    check_in: date
    check_out: date
    guests: int

class BookingResponse(BookingModel):
    id: int

    model_config = {
        "from_attributes": True
    }