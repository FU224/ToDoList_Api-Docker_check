from fastapi import FastAPI, HTTPException

from app.schemas.task import TaskCreate
from app.services.db import init_db
from app.services.joke_service import get_programming_joke
from app.services.task_service import (
    create_task,
    delete_task_by_id,
    get_all_tasks,
    get_unfinished_tasks,
    toggle_task_status,
)

app = FastAPI(title="Todo List API")


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/")
def root():
    return {"message": "Todo List API is running"}


@app.get("/tasks")
def read_tasks():
    return get_all_tasks()


@app.get("/tasks/unfinished")
def read_unfinished_tasks():
    return get_unfinished_tasks()


@app.post("/tasks")
def add_task(task: TaskCreate):
    return create_task(task.title)


@app.patch("/tasks/{task_id}/status")
def update_task_status(task_id: int):
    task = toggle_task_status(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    deleted = delete_task_by_id(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted."}


@app.get("/joke")
def joke():
    return get_programming_joke()
