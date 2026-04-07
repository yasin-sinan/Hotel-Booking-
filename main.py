from fastapi import FastAPI
from contextlib import asynccontextmanager

# We import database models.
from db import models
from db.database import engine

# We import all routers
from routers.user import router as user_router
from routers.booking import router as booking_router
from routers.preferences import router as preferences_router
from routers.hotel import router as hotel_router




# Lifespan:  Create tables when app starts up.
@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield

# FastAPI app
app = FastAPI(
    title="Hotel Booking API",
    version="1.0.0",
    lifespan=lifespan
)

# We include routers.
app.include_router(user_router)
app.include_router(preferences_router)
app.include_router(booking_router)
app.include_router(hotel_router)

# Basic test end point to see whether the app is alive :)
@app.get("/")
def root():
    title = "Hotel Booking API is running , this is just for testing purpose."
    return {"message": "Welcome to Hotel booking API. It is running."}