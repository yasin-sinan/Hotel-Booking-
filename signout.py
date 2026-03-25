from fastapi import FastAPI

app = FastAPI()

@app.post("/logout",
          tags=['Log Out'],
          summary='This is Log Out section.',
          description='This function simulates log out feature.')


def logout():
    return {"message": "You have logged out successfully."}
