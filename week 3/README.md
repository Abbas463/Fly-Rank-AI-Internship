# Task API - SQLite Persistence

A REST API for managing a to-do list with full CRUD operations, now backed by SQLite for persistent data storage. Built with Python FastAPI.

## Features

- Create, read, update, and delete tasks
- **SQLite database for persistent storage** (data survives restarts)
- Input validation
- Proper HTTP status codes
- Interactive Swagger UI documentation at `/docs`

## Why SQLite?

SQLite was chosen for this assignment because:
- **Zero configuration** - No separate database server required
- **Lightweight** - Single file database (tasks.db)
- **Portable** - Database file can be easily copied or moved
- **Perfect for learning** - Simple to understand and debug
- **Built into Python** - No additional installation needed

## Architecture

This project demonstrates clean architecture with repository pattern:

- **Service layer** (FastAPI routes) - unchanged from Week 2
- **Repository layer** (SQLiteTaskRepository) - implements data access
- **Storage swap** - only the repository changed; service and routes remain identical

This proves that proper layering allows storage changes without affecting business logic.

## Installation & Running

### Prerequisites
- Python 3.7+
- pip

### Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python -m uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

The first time you run the application, it will automatically:
- Create the `tasks.db` database file
- Create the `tasks` table
- Insert three example tasks (Buy groceries, Walk the dog, Finish homework)

## Database Location

The SQLite database file is stored at:
```
tasks.db
```

This file is created automatically in the same directory as the application.

## API Endpoints

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| GET | `/` | API information | 200 |
| GET | `/health` | Health check | 200 |
| GET | `/tasks` | List all tasks | 200 |
| GET | `/tasks/{id}` | Get a single task by ID | 200, 404 |
| POST | `/tasks` | Create a new task | 201, 400 |
| PUT | `/tasks/{id}` | Update a task | 200, 400, 404 |
| DELETE | `/tasks/{id}` | Delete a task | 204, 404 |

## Database Schema

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done BOOLEAN DEFAULT 0
);
```

## Example SQL Queries

### List every task:
```sql
SELECT * FROM tasks;
```

### Show only completed tasks:
```sql
SELECT * FROM tasks WHERE done = 1;
```

### Count all tasks:
```sql
SELECT COUNT(*) FROM tasks;
```

### Mark every task as completed:
```sql
UPDATE tasks SET done = 1;
```

### Delete all completed tasks:
```sql
DELETE FROM tasks WHERE done = 1;
```

## Example curl Output

### Create a task
```bash
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
```

Response:
```
HTTP/1.1 201 Created
content-type: application/json

{"id":1,"title":"Buy milk","done":false}
```

### Get all tasks
```bash
curl -i http://localhost:8000/tasks
```

Response:
```
HTTP/1.1 200 OK
content-type: application/json

[{"id":1,"title":"Buy milk","done":false}]
```

### Update a task
```bash
curl -i -X PUT http://localhost:8000/tasks/1 -H "Content-Type: application/json" -d '{"done":true}'
```

Response:
```
HTTP/1.1 200 OK
content-type: application/json

{"id":1,"title":"Buy milk","done":true}
```

### Delete a task
```bash
curl -i -X DELETE http://localhost:8000/tasks/1
```

Response:
```
HTTP/1.1 204 No Content
```

## Swagger UI

Interactive API documentation is available at `http://localhost:8000/docs`

## Persistence Proof

**Test: Create data, restart server**
```bash
# Create a task
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Test persistence"}'

# Stop the server (Ctrl+C)
# Start the server again
python -m uvicorn main:app --reload

# Task still exists
curl http://localhost:8000/tasks
```

## Git Commits

This project was built in stages, with one commit per stage:
- Week 3: Stage 0: create SQLite database
- Week 3: Stage 1: database read endpoints
- Week 3: Stage 2: insert into database
- Week 3: Stage 3: update and delete with SQL
- Week 3: Stage 4: explored SQLite
- Week 3: Stage 5: database documentation
