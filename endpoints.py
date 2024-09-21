from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from enum import Enum

app = FastAPI()


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class Task(BaseModel):
    id: int
    name: str
    description: str
    status: TaskStatus = TaskStatus.pending


# Database & ID creation
tasks: Dict[int, Task] = {}
current_id = 1


@app.get("/")
async def root():
    return {"message": "Hi mom!"}


# Create a task
@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    global current_id
    task.id = current_id
    tasks[current_id] = task
    current_id += 1
    return task


# Get all tasks
@app.get("/tasks/", response_model=list[Task])
async def read_tasks():
    return list(tasks.values())


# Get especified task by ID
@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    if task_id in tasks:
        return tasks[task_id]  # Busca rápida no dicionário
    raise HTTPException(status_code=404, detail="Task not found")


# Update a task
@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    if task_id in tasks:
        tasks[task_id] = task
        return task
    raise HTTPException(status_code=404, detail="Task not found")


# Delete a task
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    if task_id in tasks:
        del tasks[task_id]
        return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
