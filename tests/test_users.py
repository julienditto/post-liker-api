from app.schemas import UserReturn
from app.schemas import Token
from jose import jwt
from os import environ
import pytest


def test_create_user(client):
    res = client.post("/users/", 
    json={"email": "user@email.com", "password": "password"})
    new_user = UserReturn(**res.json())
    assert new_user.email == "user@email.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']}
    )
    login_res = Token(**res.json())
    SECRET_KEY=environ.get('SECRET_KEY')
    ALGOIRTHM=environ.get('ALGORITHM')
    payload = jwt.decode(login_res.access_token, SECRET_KEY, algorithms=[ALGOIRTHM])
    id: str = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

def test_incorrent_login(test_user, client):
    res = client.post("/login", 
                      data={"username": test_user["email"], 
                            "password": "wrongPassword"})
    assert res.status_code == 403
    assert res.json().get("detail") == "Invalid Credentials"