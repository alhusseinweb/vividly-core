"""
Project API tests
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Project
from utils.security import hash_password, create_access_token
import uuid

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


@pytest.fixture
def test_user():
    """Create test user"""
    db = TestingSessionLocal()
    user = User(
        id=str(uuid.uuid4()),
        email="test@example.com",
        password_hash=hash_password("password123"),
        first_name="Test",
        last_name="User",
        is_active=True,
        email_verified=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_token(test_user):
    """Create test token"""
    return create_access_token(test_user.id)


def test_create_project(test_token):
    """Test creating a project"""
    response = client.post(
        "/api/projects",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "name": "Test Project",
            "description": "A test project",
            "vibe_description": "Modern design with vibrant colors and smooth animations",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["status"] == "draft"


def test_list_projects(test_token):
    """Test listing projects"""
    # Create a project first
    client.post(
        "/api/projects",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "name": "Test Project",
            "description": "A test project",
            "vibe_description": "Modern design with vibrant colors",
        },
    )

    # List projects
    response = client.get(
        "/api/projects",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert len(data["projects"]) == 1


def test_get_project(test_token):
    """Test getting a specific project"""
    # Create a project
    create_response = client.post(
        "/api/projects",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "name": "Test Project",
            "description": "A test project",
            "vibe_description": "Modern design with vibrant colors",
        },
    )
    project_id = create_response.json()["id"]

    # Get project
    response = client.get(
        f"/api/projects/{project_id}",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == project_id
    assert data["name"] == "Test Project"


def test_get_project_not_found(test_token):
    """Test getting non-existent project"""
    response = client.get(
        "/api/projects/nonexistent-id",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    assert response.status_code == 404


def test_update_project(test_token):
    """Test updating a project"""
    # Create a project
    create_response = client.post(
        "/api/projects",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "name": "Test Project",
            "description": "A test project",
            "vibe_description": "Modern design with vibrant colors",
        },
    )
    project_id = create_response.json()["id"]

    # Update project
    response = client.put(
        f"/api/projects/{project_id}",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "name": "Updated Project",
            "description": "Updated description",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Project"


def test_delete_project(test_token):
    """Test deleting a project"""
    # Create a project
    create_response = client.post(
        "/api/projects",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "name": "Test Project",
            "description": "A test project",
            "vibe_description": "Modern design with vibrant colors",
        },
    )
    project_id = create_response.json()["id"]

    # Delete project
    response = client.delete(
        f"/api/projects/{project_id}",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    assert response.status_code == 200

    # Verify deletion
    get_response = client.get(
        f"/api/projects/{project_id}",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    assert get_response.status_code == 404


def test_duplicate_project(test_token):
    """Test duplicating a project"""
    # Create a project
    create_response = client.post(
        "/api/projects",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "name": "Test Project",
            "description": "A test project",
            "vibe_description": "Modern design with vibrant colors",
        },
    )
    project_id = create_response.json()["id"]

    # Duplicate project
    response = client.post(
        f"/api/projects/{project_id}/duplicate",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["new_id"] != project_id
    assert "Copy" in data["new_project"]["name"]


def test_publish_project(test_token):
    """Test publishing a project"""
    # Create a project
    create_response = client.post(
        "/api/projects",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "name": "Test Project",
            "description": "A test project",
            "vibe_description": "Modern design with vibrant colors",
        },
    )
    project_id = create_response.json()["id"]

    # Publish project
    response = client.post(
        f"/api/projects/{project_id}/publish",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "domain": "test.example.com",
            "enable_analytics": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "published"


def test_archive_project(test_token):
    """Test archiving a project"""
    # Create a project
    create_response = client.post(
        "/api/projects",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "name": "Test Project",
            "description": "A test project",
            "vibe_description": "Modern design with vibrant colors",
        },
    )
    project_id = create_response.json()["id"]

    # Archive project
    response = client.post(
        f"/api/projects/{project_id}/archive",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    assert response.status_code == 200


def test_export_project(test_token):
    """Test exporting a project"""
    # Create a project
    create_response = client.post(
        "/api/projects",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "name": "Test Project",
            "description": "A test project",
            "vibe_description": "Modern design with vibrant colors",
        },
    )
    project_id = create_response.json()["id"]

    # Export project
    response = client.post(
        f"/api/projects/{project_id}/export",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "format": "json",
            "include_assets": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["format"] == "json"


def test_unauthorized_access(test_token):
    """Test unauthorized access to project"""
    # Create a project with first user
    create_response = client.post(
        "/api/projects",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "name": "Test Project",
            "description": "A test project",
            "vibe_description": "Modern design with vibrant colors",
        },
    )
    project_id = create_response.json()["id"]

    # Create another user
    db = TestingSessionLocal()
    user2 = User(
        id=str(uuid.uuid4()),
        email="user2@example.com",
        password_hash=hash_password("password123"),
        first_name="User",
        last_name="Two",
        is_active=True,
        email_verified=True,
    )
    db.add(user2)
    db.commit()
    token2 = create_access_token(user2.id)

    # Try to access project with second user
    response = client.get(
        f"/api/projects/{project_id}",
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert response.status_code == 403
