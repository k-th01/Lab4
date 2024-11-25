from fastapi import FastAPI, HTTPException, Depends, Request
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Load secret token from .env file
SECRET_TOKEN = os.getenv("SECRET_TOKEN")

# Data storage for tasks
task_store = {
    "alpha": [
        {"id": 1, "title": "Task A", "description": "Learn FastAPI basics", "completed": False}
    ],
    "beta": [
        {"id": 1, "title": "Task B", "description": "Refactor To-Do App", "completed": False}
    ],
}

# Dependency to authenticate requests
def authenticate_request(req: Request):
    token = req.headers.get("my_secret_token")
    if token != f"Bearer {SECRET_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token

# Helper functions for task operations
def retrieve_tasks(api_version: str):
    tasks = task_store[api_version]
    if not tasks:
        raise HTTPException(status_code=204, detail="No tasks found")
    return {"status": "success", "data": tasks}

def retrieve_task_by_id(api_version: str, task_id: int):
    tasks = task_store[api_version]
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "success", "data": task}

def add_task(api_version: str, title: str, description: str):
    tasks = task_store[api_version]
    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "completed": False,
    }
    tasks.append(new_task)
    return {"status": "success", "data": new_task}

def remove_task(api_version: str, task_id: int):
    tasks = task_store[api_version]
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks.remove(task)
    return {"status": "success", "message": "Task removed successfully"}

def modify_task(api_version: str, task_id: int, title: str = None, description: str = None, completed: bool = None):
    tasks = task_store[api_version]
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if title is not None:
        task["title"] = title
    if description is not None:
        task["description"] = description
    if completed is not None:
        task["completed"] = completed
    return {"status": "success", "data": task}

# Alpha API Endpoints
@app.get("/alpha/", dependencies=[Depends(authenticate_request)])
def alpha_root():
    return {"message": "Welcome to Alpha API"}

@app.get("/alpha/tasks/")
def get_alpha_tasks():
    return retrieve_tasks("alpha")

@app.get("/alpha/tasks/{task_id}")
def get_alpha_task_by_id(task_id: int):
    return retrieve_task_by_id("alpha", task_id)

@app.post("/alpha/tasks/", status_code=201)
def create_alpha_task(title: str, description: str):
    return add_task("alpha", title, description)

@app.delete("/alpha/tasks/{task_id}", status_code=204)
def delete_alpha_task(task_id: int):
    return remove_task("alpha", task_id)

@app.patch("/alpha/tasks/{task_id}", status_code=204)
def update_alpha_task(task_id: int, title: str = None, description: str = None, completed: bool = None):
    return modify_task("alpha", task_id, title, description, completed)

# Beta API Endpoints
@app.get("/beta/", dependencies=[Depends(authenticate_request)])
def beta_root():
    return {"message": "Welcome to Beta API"}

@app.get("/beta/tasks/")
def get_beta_tasks():
    return retrieve_tasks("beta")

@app.get("/beta/tasks/{task_id}")
def get_beta_task_by_id(task_id: int):
    return retrieve_task_by_id("beta", task_id)

@app.post("/beta/tasks/", status_code=201)
def create_beta_task(title: str, description: str):
    return add_task("beta", title, description)

@app.delete("/beta/tasks/{task_id}", status_code=204)
def delete_beta_task(task_id: int):
    return remove_task("beta", task_id)

@app.patch("/beta/tasks/{task_id}", status_code=204)
def update_beta_task(task_id: int, title: str = None, description: str = None, completed: bool = None):
    return modify_task("beta", task_id, title, description, completed)
