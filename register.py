from main import app
import database

@app.post("/register")
def register(email: str, password: str):
    if any(user["email"] == email for user in database.users_email):
        return {"message": f"{email} already exists"}

    database.users_email.append({"email": email, "password": password})
    database.current_user["email"] = email
    database.current_user["password"] = password

    return {"message": f"{email} registered successfully"}