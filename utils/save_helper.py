"""
Save Helper Module
Handles saving and loading tasks to/from SQLite database.
"""

import sqlite3
import os

def get_db_path():
    """Get the path to the SQLite database file."""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "todo.db")

def init_database():
    """Initialize the database and create the todos table if it doesn't exist."""
    db_path = get_db_path()
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    try:
        with sqlite3.connect(db_path) as conn:
            # Check if old schema exists and needs migration
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='todos'")
            table_exists = cursor.fetchone()
            
            if table_exists:
                # Check if old schema (has 'text' and 'completed' columns)
                cursor.execute("PRAGMA table_info(todos)")
                columns = [col[1] for col in cursor.fetchall()]
                if 'text' in columns or 'completed' in columns:
                    # Drop old table and create new one
                    conn.execute('DROP TABLE todos')
            
            # Create new schema with title, status, description
            conn.execute('''
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    status TEXT DEFAULT 'todo',
                    description TEXT DEFAULT ''
                )
            ''')
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")

def load_tasks():
    """
    Load all tasks from SQLite database.
    
    Returns:
        list: List of task dictionaries with id, title, status, and description fields
    """
    init_database()  # Ensure database exists
    
    try:
        with sqlite3.connect(get_db_path()) as conn:
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, title, status, description FROM todos ORDER BY id")
            rows = cursor.fetchall()
            
            return [{"id": row["id"], "title": row["title"], "status": row["status"], "description": row["description"]} 
                   for row in rows]
    except sqlite3.Error as e:
        print(f"Error loading tasks: {e}")
        return []
        print(f"Error loading tasks: {e}")
        return []

def save_tasks(tasks_list):
    """
    Legacy function for compatibility - not used with SQLite approach.
    Individual operations (add, edit, delete) handle database updates directly.
    """
    # This function is kept for compatibility but not used in SQLite approach
    pass