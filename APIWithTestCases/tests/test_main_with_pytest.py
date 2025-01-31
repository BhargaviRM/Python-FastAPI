import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import MagicMock, patch
from fastapi import status
from fastapi.testclient import TestClient
from fastapiEx.database import get_db
from fastapiEx.main import app
from fastapiEx.models import Task


@pytest.fixture
def client():
    """Fixture to provide a TestClient instance."""
    client = TestClient(app)
    yield client


@pytest.fixture(autouse=True)
def mock_db_session():
    """Fixture to mock the database session."""
    mock_session = MagicMock()
    app.dependency_overrides[get_db] = lambda: mock_session
    yield mock_session
    app.dependency_overrides.clear()


def test_get_task_all(client, mock_db_session):
    """Test retrieving all tasks."""
    mock_task = Task(
        id=1,
        name="Test Task",
        description="This is a test task",
        completed=False,
    )
    mock_db_session.query.return_value.filter.return_value \
        .limit.return_value.offset.return_value.all.return_value = [
            mock_task
        ]
    response = client.get(
        "/tasks",
        params={"limit": 10, "skip": 0, "search": ""}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["name"] == "Test Task"
    assert response.json()[0]["description"] == "This is a test task"
    assert response.json()[0]["completed"] is False


def test_get_task(client, mock_db_session):
    """Test retrieving a specific task by ID."""
    mock_task = Task(
        id=1,
        name="Test Task",
        description="This is a test task",
        completed=False,
    )
    mock_db_session.query.return_value.filter.return_value \
        .first.return_value = mock_task
    response = client.get("/tasks/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Test Task"
    assert response.json()["description"] == "This is a test task"
    assert response.json()["completed"] is False


def test_get_task_not_found(client, mock_db_session):
    """Test retrieving a task that does not exist."""
    mock_db_session.query.return_value.filter.return_value\
        .first.return_value = None
    response = client.get("/tasks/999")
    assert response.status_code == 404


def test_create_task(client, mock_db_session):
    """Test creating a new task."""
    task_data = {"name": "New Task", "description": "New task description"}
    mock_task = MagicMock(
        id=1, name=task_data["name"],
        description=task_data["description"],
        completed=False
    )
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.query.return_value.filter.return_value\
        .first.return_value = mock_task
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == task_data["name"]
    assert response.json()["description"] == task_data["description"]


def test_update_task(client, mock_db_session):
    """Test updating an existing task."""
    mock_task = Task(
        id=1,
        name="Test Task",
        description="This is a test task",
        completed=False,
    )
    mock_db_session.query.return_value.filter.return_value\
        .first.return_value = mock_task
    updated_task_data = {
        "name": "Updated Task",
        "description": "Updated task description",
    }
    response = client.put("/tasks/1", json=updated_task_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == updated_task_data["name"]
    assert response.json()["description"] == updated_task_data["description"]


def test_update_task_not_found(client, mock_db_session):
    """Test updating a task that does not exist."""
    mock_db_session.query.return_value.filter.return_value\
        .first.return_value = None
    updated_task_data = {
        "name": "Updated Task",
        "description": "Updated task description",
    }
    response = client.put("/tasks/999", json=updated_task_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_task(client, mock_db_session):
    """Test deleting an existing task."""
    mock_task = Task(
        id=1,
        name="Test Task",
        description="This is a test task",
        completed=False,
    )
    mock_db_session.query.return_value.filter.return_value\
        .first.return_value = mock_task
    response = client.delete("/tasks/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_task_not_found(client, mock_db_session):
    """Test deleting a task that does not exist."""
    mock_db_session.query.return_value.filter.return_value\
        .first.return_value = None
    response = client.delete("/tasks/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@patch('fastapiEx.database.SessionLocal')
def test_get_db_success(MockSessionLocal):
    """Test the successful creation and yielding of a session."""
    mock_session = MagicMock()
    MockSessionLocal.return_value = mock_session
    db_gen = get_db()
    db = next(db_gen)
    assert db == mock_session
    db_gen.close()
    mock_session.close.assert_called_once()


@patch('fastapiEx.database.SessionLocal')
def test_get_db_after_exception(MockSessionLocal):
    """Test that the session is still closed after an exception occurs."""
    mock_session = MagicMock()
    MockSessionLocal.return_value = mock_session
    db_gen = get_db()
    next(db_gen)
    with pytest.raises(Exception):
        mock_session.close.side_effect = Exception("Unexpected error")
        db_gen.close()
    mock_session.close.assert_called_once()
