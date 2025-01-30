# schemas.py
from pydantic import BaseModel
from typing import Optional


class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    completed: bool = False


# TaskCreate is used when creating a new task (inherits TaskBase)
class TaskCreate(TaskBase):
    pass


# TaskUpdate is used for updating an existing task (inherits TaskBase)
class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    class Config:
        orm_mode = True


# Task is the output model, which includes the id of the task (inherits TaskBase)
class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True
