from fastapi import FastAPI

app = FastAPI()

users_email = [
    {"email": "zeki.tazegul@motopp.nl", "password": "123456"},
    {"email": "samaneh.noori@motopp.nl", "password": "654321"}
]

current_user = {"email": None, "password": None}

@app.post("/register")
def register(email: str, password: str):
    if any(user["email"] == email for user in users_email):
        return {"message": f"{email} already exists"}

    users_email.append({"email": email, "password": password})
    current_user["email"] = email
    current_user["password"] = password

    return {"message": f"{email} registered successfully"}