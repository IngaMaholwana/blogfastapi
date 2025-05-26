from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
import pytest

# Test configuration
@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from app.main import app
    return TestClient(app)

@pytest.fixture
def create_user(client):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    response = client.post("/users/register", json=user_data)
    return response.json()

def test_user_registration(client):
    user_data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "newpassword"
    }
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == user_data["username"]

def test_user_login(client, create_user):
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post("/users/token", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_user_login_incorrect_password(client, create_user):
    login_data = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    response = client.post("/users/token", data=login_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"

def test_user_login_nonexistent_user(client):
    login_data = {
        "username": "nonexistent",
        "password": "password"
    }
    response = client.post("/users/token", data=login_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"