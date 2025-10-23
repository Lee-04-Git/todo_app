"""
Delete Helper Module
Handles deleting tasks from the todo database.
"""

import sqlite3
from .save_helper import get_db_path

def delete_task(task_id):
    """
    Delete a task from the SQLite database.
    
    Args:
        task_id (int): The ID of the task to delete
    
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        conn = sqlite3.connect(get_db_path(), isolation_level=None)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id = ?", (task_id,))
        row_count = cursor.rowcount
        conn.close()
        return row_count > 0  # Returns True if a row was deleted
    except sqlite3.Error as e:
        print(f"Error deleting task: {e}")
        return False

def clear_completed_tasks():
    """
    Remove all tasks with 'done' status from the SQLite database.
    
    Returns:
        int: Number of tasks deleted
    """
    try:
        conn = sqlite3.connect(get_db_path(), isolation_level=None)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE status = 'done'")
        row_count = cursor.rowcount
        conn.close()
        return row_count  # Returns number of deleted rows
    except sqlite3.Error as e:
        print(f"Error clearing completed tasks: {e}")
        return 0