from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta

# Import های داخلی پروژه
from auth.auth import create_access_token, SECRET_KEY, ALGORITHM, oauth2_scheme
from db.database import get_db
from db.models import User
from schemas.user import RegisterModel, UserResponse, MessageResponse

# اصلاح مهم: Import کردن CryptContext برای حل NameError
from passlib.context import CryptContext

# -------------------------
# PASSWORD ENCRYPTION
# -------------------------
# استفاده از pbkdf2_sha256 برای حل قطعی مشکل محدودیت 72 کاراکتر در مک
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str):
    """هش کردن پسورد بدون محدودیت طول کاراکتر"""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """تایید پسورد وارد شده با هش ذخیره شده در دیتابیس"""
    return pwd_context.verify(plain_password, hashed_password)

# -------------------------
# AUTH (CURRENT USER)
# -------------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# -------------------------
# ROUTER CONFIG
# -------------------------
router = APIRouter(
    prefix="/user",
    tags=["User Operations"]
)

# -------------------------
# REGISTER
# -------------------------
@router.post("/register", response_model=UserResponse)
def register(user: RegisterModel, db: Session = Depends(get_db)):
    # بررسی تکراری نبودن ایمیل
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # ساخت یوزر جدید با پسورد هش شده
    new_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# -------------------------
# LOGIN
# -------------------------
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # در OAuth2، فیلد ایمیل در متغیر username قرار می‌گیرد
    db_user = db.query(User).filter(User.email == form_data.username).first()

    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # ساخت توکن دسترسی
    access_token = create_access_token(data={"sub": db_user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# -------------------------
# DELETE USER
# -------------------------
@router.delete("/delete", response_model=MessageResponse)
def delete_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db.delete(current_user)
    db.commit()
    return {"message": "User deleted successfully"}