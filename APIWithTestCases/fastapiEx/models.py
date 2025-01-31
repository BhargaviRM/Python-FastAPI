"""
This module defines the SQLAlchemy model for the Task entity.

The Task class represents a task in the application, with attributes
for the task's ID, name, description, completion status, and creation
timestamp. It is mapped to the 'tasks' table in the database.
"""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
# from sqlalchemy.sql import func

from fastapiEx.database import Base


class Task(Base):
    """
    SQLAlchemy model representing a task.

    Attributes:
        id (int): Unique identifier for the task (primary key).
        name (str): Name of the task (required).
        description (str): Description of the task (optional).
        completed (bool): Completion status of the task (default is False).
        created_at (datetime): Timestamp of when the task was created.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, server_default="FALSE", nullable=False)
    # created_at = Column(
    #     TIMESTAMP(timezone=True),
    #     nullable=False, server_default=text("now()")
    # )
    # created_at = Column(
    #     TIMESTAMP, server_default=func.current_timestamp, nullable=False
    # )
    created_at = Column(
            TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False
        )
