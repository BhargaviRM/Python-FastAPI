from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas
from .database import get_db

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# Get all tasks
@router.get("/", response_model=List[schemas.Task])
def get_tasks(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    tasks = (
        db.query(models.Task)
        .filter(models.Task.name.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return tasks


# Create a new task
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# Get a task by ID
@router.get("/{id}", response_model=schemas.Task)
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id: {id} not found",
        )
    return task


# Delete a task by ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id: {id} does not exist",
        )

    db.delete(task)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a task by ID
@router.put("/{id}", response_model=schemas.Task)
def update_task(
    id: int, updated_task: schemas.TaskUpdate, db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id: {id} does not exist",
        )

    for key, value in updated_task.dict(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task
