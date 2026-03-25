from main import app
import database

@app.post("/login")
def login(email: str, password: str):
    for user_info in database.users_email:
        if user_info["email"] == email:
            if user_info["password"] == password:
                database.current_user["email"] = email
                database.current_user["password"] = password
                return {"message": f"{email} login successfully"}
            else:
                return {"message": f"password for {email} incorrect"}

    return {"message": f"{email} not found"}