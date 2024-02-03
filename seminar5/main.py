from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Task(BaseModel):
    title: str
    description: str
    status: bool = False

tasks_db = []

@app.get("/")
async def root():
    return {"Hello": "world"}

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return tasks_db

@app.get("/tasks/{id}", response_model=Task)
async def get_task(id: int):
    try:
        return tasks_db[id]
    except IndexError:
        raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks", response_model=Task)
async def add_task(task: Task):
    tasks_db.append(task)
    return task

@app.put("/tasks/{id}", response_model=Task)
async def update_task(id: int, task: Task):
    try:
        tasks_db[id] = task
        return task
    except IndexError:
        raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{id}")
async def delete_task(id: int):
    try:
        del tasks_db[id]
        return {"msg": "Task deleted successfully"}
    except IndexError:
        raise HTTPException(status_code=404, detail="Task not found")
            