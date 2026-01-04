"""
Authentication API tests
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User
from utils.security import hash_password
import json

# Test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup():
    """Clean up database before each test"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def test_register_user():
    """Test user registration"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["first_name"] == "Test"
    assert "id" in data


def test_register_user_duplicate_email():
    """Test registration with duplicate email"""
    # Register first user
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        },
    )

    # Try to register with same email
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "password456",
            "first_name": "Another",
            "last_name": "User",
        },
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_register_user_invalid_email():
    """Test registration with invalid email"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "invalid-email",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    assert response.status_code == 422


def test_register_user_weak_password():
    """Test registration with weak password"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "weak",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    assert response.status_code == 422


def test_login_user():
    """Test user login"""
    # Register user
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        },
    )

    # Login
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["email"] == "test@example.com"


def test_login_user_invalid_password():
    """Test login with invalid password"""
    # Register user
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        },
    )

    # Login with wrong password
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]


def test_login_user_not_found():
    """Test login with non-existent user"""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 401


def test_refresh_token():
    """Test token refresh"""
    # Register and login
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        },
    )

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123",
        },
    )
    refresh_token = login_response.json()["refresh_token"]

    # Refresh token
    response = client.post(
        "/api/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_refresh_token_invalid():
    """Test refresh with invalid token"""
    response = client.post(
        "/api/auth/refresh",
        json={"refresh_token": "invalid_token"},
    )
    assert response.status_code == 401


def test_get_current_user():
    """Test getting current user"""
    # Register and login
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        },
    )

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123",
        },
    )
    access_token = login_response.json()["access_token"]

    # Get current user
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"


def test_get_current_user_unauthorized():
    """Test getting current user without token"""
    response = client.get("/api/auth/me")
    assert response.status_code == 401


def test_logout_user():
    """Test user logout"""
    # Register and login
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        },
    )

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123",
        },
    )
    access_token = login_response.json()["access_token"]

    # Logout
    response = client.post(
        "/api/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200


def test_get_sessions():
    """Test getting user sessions"""
    # Register and login
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        },
    )

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123",
        },
    )
    access_token = login_response.json()["access_token"]

    # Get sessions
    response = client.get(
        "/api/auth/sessions",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "sessions" in data
    assert len(data["sessions"]) > 0


def test_revoke_all_sessions():
    """Test revoking all sessions"""
    # Register and login
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        },
    )

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123",
        },
    )
    access_token = login_response.json()["access_token"]

    # Revoke all sessions
    response = client.post(
        "/api/auth/revoke-all-sessions",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
