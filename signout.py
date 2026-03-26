from fastapi import APIRouter

signout_router = APIRouter()

@signout_router.post("/")
def logout():
    # Simulate logout
    return {"message": "You have logged out successfully."}