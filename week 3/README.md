# Task API - PostgreSQL Persistence

A REST API for managing a to-do list with full CRUD operations, now backed by PostgreSQL for persistent data storage. Built with Python FastAPI and Docker.

## Features

- Create, read, update, and delete tasks
- **PostgreSQL database for persistent storage** (data survives restarts)
- Input validation
- Proper HTTP status codes
- Interactive Swagger UI documentation at `/docs`
- **Docker Compose for one-command startup** (app + database together)

## Architecture

This project demonstrates clean architecture with repository pattern:

- **Service layer** (FastAPI routes) - unchanged from Week 2
- **Repository layer** (PostgresTaskRepository) - implements data access
- **Storage swap** - only the repository changed; service and routes remain identical

This proves that proper layering allows storage changes without affecting business logic.

## Installation & Running

### Prerequisites
- Docker and Docker Compose

### Quick Start

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Start the entire stack with one command:
```bash
docker compose up --build
```

This will:
- Start PostgreSQL with persistent volume
- Run the init.sql script to create the tasks table
- Start the FastAPI application
- Wait for database to be healthy before starting app

The API will be available at `http://localhost:8000`

### Manual Setup (Alternative)

If you want to run locally without Docker:

1. Start PostgreSQL:
```bash
docker run -d --name taskdb_postgres \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=taskdb \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:15-alpine
```

2. Run init script:
```bash
docker exec -i taskdb_postgres psql -U user -d taskdb < init.sql
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python -m uvicorn main:app --reload
```

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

## Persistence Proof

**Test 1: Create data, restart app**
```bash
# Create a task
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Test persistence"}'

# Restart app container (docker compose restart app)
# Task still exists
curl http://localhost:8000/tasks
```

**Test 2: Create data, restart entire stack**
```bash
# Create a task
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Test full restart"}'

# Stop everything: docker compose down
# Start everything: docker compose up
# Task still exists (data in postgres_data volume)
curl http://localhost:8000/tasks
```

**Verification:**
- Data persists across app restarts (proves database connection)
- Data persists across container restarts (proves Docker volume)
- Service and routes unchanged from Week 2 (proves architecture)

## Database Schema

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    done BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_title ON tasks(title);
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

## Git Commits

This project was built in stages, with one commit per stage:
- Week 3: Stage 0: project structure and Docker setup
- Week 3: Stage 1: database schema and Postgres repository
- Week 3: Stage 2: integrate repository and persistence proof
