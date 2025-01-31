"""
Unit tests for the Task API endpoints.
It uses the unittest framework to define and run the tests.
"""

import unittest
from unittest.mock import MagicMock, patch
from fastapi import status
from fastapi.testclient import TestClient
from fastapiEx.database import get_db
from fastapiEx.main import app
from fastapiEx.models import Task


class TestTaskEndpoints(unittest.TestCase):
    """
    Test case for the Task API endpoints.

    This class contains unit tests for verifying the functionality
    of the Task-related API endpoints, including creating, retrieving,
    updating, and deleting tasks.
    """
    def setUp(self):
        """
        Set up the test client and mock database session before each test.

        This method initializes the TestClient and sets up a mock
        database session to be used in the tests.
        """
        self.client = TestClient(app)
        self.mock_db_session = MagicMock()
        app.dependency_overrides[get_db] = self.mock_get_db

    def tearDown(self):
        """
        Clean up after each test.

        This method clears the dependency overrides to ensure that
        each test runs with a fresh state.
        """
        app.dependency_overrides.clear()

    def mock_get_db(self):
        """
        Mock the database session for testing.

        This method returns a MagicMock object that simulates the
        behavior of a database session, allowing for controlled
        testing of database interactions without requiring a real
        database connection.

        Returns:
            MagicMock: A mock database session object.
        """
        return self.mock_db_session

    def test_get_task_all(self):
        """
        Test retrieving all tasks.

        This method tests the API endpoint for getting all tasks
        and verifies that the response contains the expected task data.
        """
        mock_task = Task(
            id=1,
            name="Test Task",
            description="This is a test task",
            completed=False,
        )
        self.mock_db_session.query.return_value.filter.return_value \
            .limit.return_value.offset.return_value.all.return_value = [
                mock_task
            ]
        response = self.client.get(
            "/tasks", params={"limit": 10, "skip": 0, "search": ""}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.json()[0]["name"] == "Test Task"
        assert response.json()[0]["description"] == "This is a test task"
        assert response.json()[0]["completed"] is False

    def test_get_task(self):
        """
        Test retrieving a specific task by ID.

        This method tests the API endpoint for getting a task by its
        ID and verifies that the response contains the expected task data.
        """
        mock_task = Task(
            id=1,
            name="Test Task",
            description="This is a test task",
            completed=False,
        )
        self.mock_db_session.query.return_value.filter.return_value.\
            first.return_value = (
                mock_task
            )
        response = self.client.get("/tasks/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.json()["name"] == "Test Task"
        assert response.json()["description"] == "This is a test task"
        assert response.json()["completed"] is False

    def test_get_task_not_found(self):
        """
        Test retrieving a task that does not exist.

        This method tests the API endpoint for getting a task by ID
        when the task does not exist and verifies that a 404 status
        code is returned.
        """
        self.mock_db_session.query.return_value.filter.return_value \
            .first.return_value = (
                None
            )

        response = self.client.get("/tasks/999")
        self.assertEqual(response.status_code, 404)

    def test_create_task(self):
        """
        Test creating a new task.

        This method tests the API endpoint for creating a new task
        and verifies that the response contains the expected task data
        and a 201 status code.
        """
        task_data = {"name": "New Task", "description": "New task description"}
        response = self.client.post("/tasks/", json=task_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["name"], task_data["name"])
        self.assertEqual(
            response.json()["description"], task_data["description"]
        )

    def test_update_task(self):
        """
        Test updating an existing task.

        This method tests the API endpoint for updating a task by ID
        and verifies that the response contains the updated task data
        and a 200 status code.
        """
        mock_task = Task(
            id=1,
            name="Test Task",
            description="This is a test task",
            completed=False,
        )
        self.mock_db_session.query.return_value.filter.return_value \
            .first.return_value = (
                mock_task
            )
        updated_task_data = {
            "name": "Updated Task",
            "description": "Updated task description",
        }
        response = self.client.put("/tasks/1", json=updated_task_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], updated_task_data["name"])
        self.assertEqual(
            response.json()["description"], updated_task_data["description"]
        )

    def test_update_task_not_found(self):
        """
        Test updating a task that does not exist.

        This method tests the API endpoint for updating a task by ID
        when the task does not exist and verifies that a 404 status
        code is returned.
        """
        self.mock_db_session.query.return_value.filter.return_value \
            .first.return_value = None
        updated_task_data = {
            "name": "Updated Task",
            "description": "Updated task description",
        }
        response = self.client.put("/tasks/999", json=updated_task_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_task(self):
        """
        Test deleting an existing task.

        This method tests the API endpoint for deleting a task by ID
        and verifies that a 204 status code is returned upon successful
        deletion.
        """
        mock_task = Task(
            id=1,
            name="Test Task",
            description="This is a test task",
            completed=False,
        )
        self.mock_db_session.query.return_value \
            .filter.return_value.first.return_value = (
                mock_task
            )
        response = self.client.delete("/tasks/1")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_task_not_found(self):
        """
        Test deleting a task that does not exist.

        This method tests the API endpoint for deleting a task by ID
        when the task does not exist and verifies that a 404 status
        code is returned.
        """
        self.mock_db_session.query.return_value.filter.return_value.\
            first.return_value = None
        response = self.client.delete("/tasks/999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('fastapiEx.database.SessionLocal')
    def test_get_db_success(self, MockSessionLocal):
        """Test the successful creation and yielding of a session."""
        mock_session = MagicMock()
        MockSessionLocal.return_value = mock_session
        db_gen = get_db()
        db = next(db_gen)
        self.assertEqual(db, mock_session)
        db_gen.close()
        mock_session.close.assert_called_once()

    @patch('fastapiEx.database.SessionLocal')
    def test_get_db_after_exception(self, MockSessionLocal):
        """Test that the session is still closed after an exception occurs."""
        mock_session = MagicMock()
        MockSessionLocal.return_value = mock_session
        db_gen = get_db()
        next(db_gen)
        with self.assertRaises(Exception):
            mock_session.close.side_effect = Exception("Unexpected error")
            db_gen.close()
        mock_session.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
