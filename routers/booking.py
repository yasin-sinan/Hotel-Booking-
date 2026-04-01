from fastapi import APIRouter, Depends
from auth.auth import get_current_user

router = APIRouter(
    prefix="/booking",
    tags=["Booking"]
)

@router.get("/secure")
def secure_route(current_user: str = Depends(get_current_user)):
    return {
        "message": "You are a very authorized person.",
        "user": current_user
    }