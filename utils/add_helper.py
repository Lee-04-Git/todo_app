"""
Add Helper Module
Handles adding new tasks to the todo database.
"""

import sqlite3
from .save_helper import get_db_path, init_database

def add_task(title, status='todo', description=''):
    """
    Add a new task to the SQLite database.
    
    Args:
        title (str): The title of the task
        status (str): The status of the task ('todo', 'doing', or 'done')
        description (str): The description of the task
    
    Returns:
        int: ID of the newly created task, or None if failed
    """
    if not title or not title.strip():
        return None
    
    # Validate status
    valid_statuses = ['todo', 'doing', 'done']
    if status not in valid_statuses:
        status = 'todo'
    
    init_database()  # Ensure database exists
    
    try:
        with sqlite3.connect(get_db_path()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO todos (title, status, description) VALUES (?, ?, ?)",
                (title.strip(), status, description.strip())
            )
            conn.commit()
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error adding task: {e}")
        return None