from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

import uuid

def test_register():
    random_email = f"test_{uuid.uuid4()}@example.com"
    response = client.post("/user/register", json={
        "email": random_email,
        "password": "test123",
        "full_name": "Test User"
    })
    assert response.status_code == 200

def test_register_duplicate():
    # Aynı email iki kez register edilemez
    client.post("/user/register", json={
        "email": "duplicate@example.com",
        "password": "test123",
        "full_name": "Test"
    })
    response = client.post("/user/register", json={
        "email": "duplicate@example.com",
        "password": "test123",
        "full_name": "Test"
    })
    assert response.status_code == 409

def test_login():
    client.post("/user/register", json={
        "email": "login@example.com",
        "password": "test123",
        "full_name": "Login User"
    })
    response = client.post("/user/login", data={
        "username": "login@example.com",
        "password": "test123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    response = client.post("/user/login", data={
        "username": "login@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 400
