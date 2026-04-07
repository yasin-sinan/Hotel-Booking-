from sqlalchemy import Column, Integer, String
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    full_name = Column(String, nullable=False)

    full_name = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    preferences = relationship("Preference", back_populates="user", cascade="all, delete-orphan")

class Preference(Base):
    __tablename__ = "preferences"
    __allow_unmapped__ = True  # ✅ EKLENDİ

    id = Column(Integer, primary_key=True, index=True)
    hotel_type = Column(String, nullable=True)
    room_type = Column(String, nullable=True)
    sea_view = Column(Boolean, nullable=True)
    stars = Column(Integer, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="preferences")

class Hotel(Base):
    __tablename__ = "hotels"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    hotel_type = Column(String, nullable=False)
    room_type = Column(String, nullable=False)
    sea_view = Column(Boolean, default=False)
    stars = Column(Integer, nullable=False)
    price_per_night = Column(Integer, nullable=False)

