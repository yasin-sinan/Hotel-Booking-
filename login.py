from fastapi import APIRouter
from pydantic import BaseModel

login_router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@login_router.post("/")
def login(data: LoginRequest):
    # For now, just simulate login
    return {
        "message": "User logged in successfully",
        "email": data.email
    }