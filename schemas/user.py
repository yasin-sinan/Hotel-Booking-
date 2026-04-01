from pydantic import BaseModel, EmailStr
from typing import Optional

# For Register operation
class RegisterModel(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

# For  Login operation
class LoginModel(BaseModel):
    email: EmailStr
    password: str

# What we want to user to display
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

# Simple message response
class MessageResponse(BaseModel):
    message: str