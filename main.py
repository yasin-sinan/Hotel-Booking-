from fastapi import FastAPI
from register import register_router
from login import login_router
from signout import signout_router

app = FastAPI(title="Hotel Booking API")

# Include routers with prefixes
app.include_router(register_router, prefix="/register", tags=["Register"])
app.include_router(login_router, prefix="/login", tags=["Login"])
app.include_router(signout_router, prefix="/logout", tags=["Logout"])
