import database
from fastapi import app

current_user = {"email": None, "password": None}


@app.post("/register")
def register(email: str, password: str):
    if any(user["email"] == email for user in users_email):
        return {"message": f"{email} already exists"}

    users_email.append({"email": email, "password": password})
    current_user["email"] = email
    current_user["password"] = password

    return {"message": f"{email} registered successfully"}
