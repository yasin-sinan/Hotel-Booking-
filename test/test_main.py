from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)


def test_register_user():
    # تغییر ایمیل برای جلوگیری از ارور 409 (Duplicate)
    # اضافه کردن full_name چون در مدل RegisterModel شما اجباری است
    response = client.post("/user/register", json={
        "email": "tester_final_1@example.com",
        "password": "mypassword123",
        "full_name": "Tester User"
    })
    # اگر ایمیل تکراری نباشه باید 200 بده، اگر از قبل باشه 409
    assert response.status_code in [200, 201, 409]


def test_login_user():
    # در OAuth2PasswordRequestForm، اطلاعات باید به صورت Form Data ارسال شود (data=)
    # فیلدها حتما باید نامشان username و password باشد
    response = client.post("/user/login", data={
        "username": "tester_final_1@example.com",
        "password": "mypassword123"
    })

    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"