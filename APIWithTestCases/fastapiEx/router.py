"""
This module defines the API endpoints for managing tasks in the application.

It includes routes for creating, retrieving, updating, and deleting tasks.
The endpoints interact with the database using SQLAlchemy and return
responses in accordance with the FastAPI framework.

Endpoints:
- GET /tasks: Retrieve a list of tasks.
- POST /tasks: Create a new task.
- GET /tasks/{task_id}: Retrieve a task by its ID.
- DELETE /tasks/{task_id}: Delete a task by its ID.
- PUT /tasks/{task_id}: Update a task by its ID.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapiEx import models, schemas
from fastapiEx.database import get_db

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# Get all tasks
@router.get("/", response_model=List[schemas.Task])
def get_tasks(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    """
    Retrieve a list of tasks.

    Args:
        db (Session): The database session.
        limit (int): The maximum number of tasks to return (default is 10).
        skip (int): The number of tasks to skip (for pagination, default is 0).
        search (Optional[str]): A search term to filter tasks by name
        (default is empty).

    Returns:
        List[schemas.Task]: A list of tasks matching the search criteria.
    """
    tasks = (
        db.query(models.Task)
        .filter(models.Task.name.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return tasks


# Create a new task
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task.

    Args:
        task (schemas.TaskCreate): The task data to create.
        db (Session): The database session.

    Returns:
        models.Task: The created task.
    """
    new_task = models.Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# Get a task by ID
@router.get("/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a task by its ID.

    Args:
        task_id (int): The ID of the task to retrieve.
        db (Session): The database session.

    Raises:
        HTTPException: If the task with the given ID does not exist.

    Returns:
        models.Task: The task with the specified ID.
    """
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id: {task_id} not found",
        )
    return task


# Delete a task by ID
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task by its ID.

    Args:
        task_id (int): The ID of the task to delete.
        db (Session): The database session.

    Raises:
        HTTPException: If the task with the given ID does not exist.

    Returns:
        Response: A response with a 204 status code indicating successful
        deletion.
    """
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id: {task_id} does not exist",
        )

    db.delete(task)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a task by ID
@router.put("/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int,
    updated_task: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a task by its ID.

    Args:
        task_id (int): The ID of the task to update.
        updated_task (schemas.TaskUpdate): The updated task data.
        db (Session): The database session.

    Raises:
        HTTPException: If the task with the given ID does not exist.

    Returns:
        models.Task: The updated task.
    """
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id: {task_id} does not exist",
        )

    for key, value in updated_task.dict(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task
