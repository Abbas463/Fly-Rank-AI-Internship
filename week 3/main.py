from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from repository import PostgresTaskRepository, TaskCreate, TaskUpdate

app = FastAPI()

# Postgres repository
repository = PostgresTaskRepository()

@app.get("/")
def read_root():
    """Returns API information"""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    """List all tasks"""
    return repository.get_all()

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Get a single task by ID"""
    task = repository.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    """Create a new task"""
    if not task.title or task.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title is required")
    return repository.create(task)

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    """Update an existing task"""
    if task_update.title is not None and task_update.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    updated_task = repository.update(task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return updated_task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete a task"""
    deleted = repository.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
