from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# In-memory "database"
tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": True},
    {"id": 3, "title": "Write README", "done": False}
]
next_id = 4

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

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
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Get a single task by ID"""
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    """Create a new task"""
    global next_id
    if not task.title or task.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title is required")
    new_task = {"id": next_id, "title": task.title, "done": False}
    tasks.append(new_task)
    next_id += 1
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    """Update an existing task"""
    for task in tasks:
        if task["id"] == task_id:
            if task_update.title is not None:
                if task_update.title.strip() == "":
                    raise HTTPException(status_code=400, detail="Title cannot be empty")
                task["title"] = task_update.title
            if task_update.done is not None:
                task["done"] = task_update.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete a task"""
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
