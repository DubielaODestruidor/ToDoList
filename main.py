from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Task(BaseModel):
    id: int = None
    name: str = None
    description: str = None
    done: bool = None


tasks = []


@app.get("/tasks/", response_model=Task)
async def create_task(task: Task):
    tasks.append(task)
    return task


@app.get("/tasks/", response_model=List[Task])
async def read_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    for index, t in enumerate(tasks):
        if t.id == task_id:
            tasks[index] = task
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            del tasks[index]
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
