from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Hotel, User
from auth.auth import get_current_admin
from schemas.hotel import HotelRequest, HotelResponse

router = APIRouter(
    prefix="/hotel",
    tags=["Hotel"]
)

@router.post("/add", response_model=HotelResponse)
def add_hotel(
    hotel: HotelRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)  # sadece admin!
):
    new_hotel = Hotel(**hotel.model_dump())
    db.add(new_hotel)
    db.commit()
    db.refresh(new_hotel)
    return new_hotel

@router.get("/list", response_model=list[HotelResponse])
def list_hotels(db: Session = Depends(get_db)):
    return db.query(Hotel).all()