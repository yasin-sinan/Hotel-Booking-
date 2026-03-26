from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

register_router = APIRouter()

# Basit hafıza tabanlı "veritabanı"
users_db = set()


class RegisterRequest(BaseModel):
    email: str
    password: str


@register_router.post("/")
def register(data: RegisterRequest):
    if data.email in users_db:
        # Kullanıcı zaten kayıtlı
        raise HTTPException(status_code=200, detail="User already exists")

    # Yeni kullanıcıyı ekle
    users_db.add(data.email)

    return {
        "message": "User registered successfully",
        "email": data.email
    }