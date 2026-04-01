from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm
from auth.auth import create_access_token, SECRET_KEY, ALGORITHM, oauth2_scheme
from db.database import get_db
from db.models import User
from schemas.user import RegisterModel, UserResponse, MessageResponse
from passlib.context import CryptContext

# Password encryption
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------------------------
# PASSWORD FUNCTIONS
# -------------------------
def hash_password(password: str):
    truncated = password[:72]  # bcrypt limit
    return pwd_context.hash(truncated)

def verify_password(plain_password, hashed_password):
    truncated = plain_password[:72]
    return pwd_context.verify(truncated, hashed_password)

# -------------------------
# AUTH (CURRENT USER)
# -------------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
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
# ROUTER
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
    db_user = db.query(User).filter(User.email == user.email).first()

    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")

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
    db_user = db.query(User).filter(User.email == form_data.username).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# -------------------------
# LOGOUT
# -------------------------
@router.post("/logout", response_model=MessageResponse)
def logout():
    # returns only response
    return {"message": "Successfully logged out"}

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
