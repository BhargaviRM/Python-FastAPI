
# for installing FastAPI: pip install "fastapi[standard]"
# running server: uvicorn main:app --reload
# http://127.0.0.1:8000 
# for flagger (http://127.0.0.1:8000/docs)

from fastapi import FastAPI, status, Response, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Task(BaseModel):
    name: str
    task: str
    completed: bool = False


my_tasks = [
    {"id": 1, "name": "test1", "task": "test1"},
    {"id": 2, "name": "test2", "task": "test2"},
]


def find_post_index(id):
    for index, task in enumerate(my_tasks):
        if task["id"] == id:
            return index


@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/tasks")
def get_tasks():
    return {"data": my_tasks}


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(new_task: Task):
    task = new_task.dict()
    task["id"] = randrange(3, 10000)
    my_tasks.append(task)
    return {"data": task}


@app.delete("/tasks/{id}")
def delete_task(id: int):
    index = find_post_index(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found with this id {id}",
        )
    my_tasks.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/tasks/{id}")
def update_task(id: int, update_post: Task):
    index = find_post_index(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found with this id {id}",
        )
    task = update_post.dict()
    task["id"] = id
    my_tasks[index] = task
    return {"data": task}
