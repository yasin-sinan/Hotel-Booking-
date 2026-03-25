from fastapi import FastAPI

app = FastAPI()


@app.post("/login")
def login(email: str, password: str):
        if email not in users_email:
                return {"message": "user not found"}

        current_user["email"] = email
        return {"message": f"{email} login"}