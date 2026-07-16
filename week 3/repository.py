import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, List, Dict
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

class PostgresTaskRepository:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")
        if not self.db_url:
            raise ValueError("DATABASE_URL environment variable not set")
        self.connection = psycopg2.connect(self.db_url)
        self.connection.autocommit = True
    
    def get_all(self) -> List[Dict]:
        """Get all tasks"""
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT id, title, done FROM tasks ORDER BY id")
            return cursor.fetchall()
    
    def get_by_id(self, task_id: int) -> Optional[Dict]:
        """Get a single task by ID"""
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT id, title, done FROM tasks WHERE id = %s", (task_id,))
            result = cursor.fetchone()
            return result
    
    def create(self, task: TaskCreate) -> Dict:
        """Create a new task"""
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO tasks (title, done) VALUES (%s, FALSE) RETURNING id, title, done",
                (task.title,)
            )
            return cursor.fetchone()
    
    def update(self, task_id: int, task_update: TaskUpdate) -> Optional[Dict]:
        """Update an existing task"""
        updates = []
        params = []
        
        if task_update.title is not None:
            updates.append("title = %s")
            params.append(task_update.title)
        
        if task_update.done is not None:
            updates.append("done = %s")
            params.append(task_update.done)
        
        if not updates:
            return self.get_by_id(task_id)
        
        params.append(task_id)
        
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                f"UPDATE tasks SET {', '.join(updates)} WHERE id = %s RETURNING id, title, done",
                params
            )
            return cursor.fetchone()
    
    def delete(self, task_id: int) -> bool:
        """Delete a task"""
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            return cursor.rowcount > 0
    
    def close(self):
        """Close database connection"""
        self.connection.close()
