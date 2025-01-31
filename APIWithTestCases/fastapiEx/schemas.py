"""
Schemas for the FastAPI application.

This module defines Pydantic models (schemas) used for data validation
and serialization in the application. These schemas are used to define
the structure of task data for creating, updating, and retrieving tasks.

Classes:
- TaskBase: Base schema for task attributes.
- TaskCreate: Schema for creating a new task.
- TaskUpdate: Schema for updating an existing task.
- Task: Schema for representing a task with an ID.
"""

from typing import Optional
from pydantic import BaseModel


class TaskBase(BaseModel):
    """
    Base schema for task attributes.

    Attributes:
        name (str): The name of the task (required).
        description (Optional[str]): A brief description of the task
        (optional).
        completed (bool): Indicates whether the task is completed
        (default is False).
    """
    name: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.

    Inherits from TaskBase and is used when creating a new task.
    """


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.

    Attributes:
        name (Optional[str]): The updated name of the task (optional).
        description (Optional[str]): The updated description of the task
        (optional).
        completed (Optional[bool]): The updated completion status of the
        task (optional).

    Config:
        orm_mode (bool): Enables compatibility with ORM models.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    class Config:
        """
        Configuration for the TaskUpdate schema.

        Enables compatibility with ORM models by allowing the model to read
        data from ORM objects directly, which is useful when working with
        SQLAlchemy models.
        """
        orm_mode = True


class Task(TaskBase):
    """
    Schema for representing a task with an ID.

    Inherits from TaskBase and includes the task's ID.

    Attributes:
        id (int): The unique identifier for the task.

    Config:
        orm_mode (bool): Enables compatibility with ORM models.
    """
    id: int

    class Config:
        """
        Configuration for the Task schema.

        Enables compatibility with ORM models by allowing the model to read
        data from ORM objects directly, which is useful when working with
        SQLAlchemy models.
        """
        orm_mode = True
