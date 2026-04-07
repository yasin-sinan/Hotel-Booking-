from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_admin_token():
    # Admin login
    response = client.post("/user/login", data={
        "username": "admin@example.com",
        "password": "admin"
    })
    return response.json()["access_token"]

def get_user_token():
    # Normal kullanıcı login
    client.post("/user/register", json={
        "email": "normal@example.com",
        "password": "test123",
        "full_name": "Normal User"
    })
    response = client.post("/user/login", data={
        "username": "normal@example.com",
        "password": "test123"
    })
    return response.json()["access_token"]

def test_add_hotel_as_admin():
    token = get_admin_token()
    response = client.post("/hotel/add",
        json={
            "name": "Test Hotel",
            "hotel_type": "Luxury",
            "room_type": "Suite",
            "sea_view": True,
            "stars": 5,
            "price_per_night": 500
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_add_hotel_as_normal_user():
    # Normal kullanıcı hotel ekleyememeli
    token = get_user_token()
    response = client.post("/hotel/add",
        json={
            "name": "Test Hotel",
            "hotel_type": "Luxury",
            "room_type": "Suite",
            "sea_view": True,
            "stars": 5,
            "price_per_night": 500
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403

