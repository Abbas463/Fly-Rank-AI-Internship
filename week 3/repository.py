import sqlite3
from typing import Optional, List, Dict
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

class SQLiteTaskRepository:
    def __init__(self, db_path: str = "tasks.db"):
        self.db_path = db_path
        self._initialize_database()
    
    def _get_connection(self):
        """Get a fresh connection for each operation"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _initialize_database(self):
        """Create table and insert sample data if empty"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done BOOLEAN DEFAULT 0
            )
        """)
        
        # Check if table is empty and insert sample data
        cursor.execute("SELECT COUNT(*) FROM tasks")
        count = cursor.fetchone()[0]
        
        if count == 0:
            sample_tasks = [
                ("Buy groceries", 0),
                ("Walk the dog", 0),
                ("Finish homework", 0)
            ]
            cursor.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                sample_tasks
            )
        
        conn.commit()
        conn.close()
    
    def get_all(self) -> List[Dict]:
        """Get all tasks"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, done FROM tasks ORDER BY id")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def get_by_id(self, task_id: int) -> Optional[Dict]:
        """Get a single task by ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def create(self, task: TaskCreate) -> Dict:
        """Create a new task"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, done) VALUES (?, 0)",
            (task.title,)
        )
        cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (cursor.lastrowid,))
        row = cursor.fetchone()
        conn.commit()
        conn.close()
        return dict(row)
    
    def update(self, task_id: int, task_update: TaskUpdate) -> Optional[Dict]:
        """Update an existing task"""
        updates = []
        params = []
        
        if task_update.title is not None:
            updates.append("title = ?")
            params.append(task_update.title)
        
        if task_update.done is not None:
            updates.append("done = ?")
            params.append(task_update.done)
        
        if not updates:
            return self.get_by_id(task_id)
        
        params.append(task_id)
        
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?",
            params
        )
        conn.commit()
        conn.close()
        return self.get_by_id(task_id)
    
    def delete(self, task_id: int) -> bool:
        """Delete a task"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted
    
