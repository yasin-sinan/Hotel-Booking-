from main import app
import database

@app.post("/logout")
def logout():
    database.current_user["email"] = None
    database.current_user["password"] = None
    return {"message": "You have logged out successfully."}
