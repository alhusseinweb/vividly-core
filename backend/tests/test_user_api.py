"""
User API tests
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User
from utils.security import hash_password
from datetime import datetime

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


@pytest.fixture
def test_user():
    """Create test user"""
    db = TestingSessionLocal()
    user = User(
        id="test-user-1",
        email="test@example.com",
        password_hash=hash_password("password123"),
        first_name="Test",
        last_name="User",
        is_active=True,
        email_verified=True,
        is_admin=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_admin():
    """Create test admin"""
    db = TestingSessionLocal()
    admin = User(
        id="test-admin-1",
        email="admin@example.com",
        password_hash=hash_password("admin123"),
        first_name="Admin",
        last_name="User",
        is_active=True,
        email_verified=True,
        is_admin=True,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


def test_get_current_user(test_user):
    """Test getting current user"""
    # TODO: Implement after auth endpoints are tested
    pass


def test_get_user_by_id(test_user):
    """Test getting user by ID"""
    response = client.get(f"/api/users/{test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["first_name"] == test_user.first_name


def test_get_user_not_found():
    """Test getting non-existent user"""
    response = client.get("/api/users/non-existent-id")
    assert response.status_code == 404


def test_list_users(test_admin):
    """Test listing users"""
    # TODO: Implement after auth endpoints are tested
    pass


def test_update_user(test_user):
    """Test updating user"""
    # TODO: Implement after auth endpoints are tested
    pass


def test_change_password(test_user):
    """Test changing password"""
    # TODO: Implement after auth endpoints are tested
    pass


def test_deactivate_account(test_user):
    """Test deactivating account"""
    # TODO: Implement after auth endpoints are tested
    pass


def test_delete_account(test_user):
    """Test deleting account"""
    # TODO: Implement after auth endpoints are tested
    pass


def test_search_users(test_admin):
    """Test searching users"""
    # TODO: Implement after auth endpoints are tested
    pass


def test_get_user_stats(test_admin):
    """Test getting user statistics"""
    # TODO: Implement after auth endpoints are tested
    pass


def test_get_user_preferences(test_user):
    """Test getting user preferences"""
    # TODO: Implement after auth endpoints are tested
    pass


def test_update_user_preferences(test_user):
    """Test updating user preferences"""
    # TODO: Implement after auth endpoints are tested
    pass
