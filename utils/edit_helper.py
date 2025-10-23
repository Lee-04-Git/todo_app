"""
Edit Helper Module
Handles editing existing tasks in the todo database.
"""

import sqlite3
from .save_helper import get_db_path, init_database

def edit_task(task_id, title=None, status=None, description=None):
    """
    Edit an existing task in the SQLite database.
    
    Args:
        task_id (int): The ID of the task to edit
        title (str, optional): The new title for the task
        status (str, optional): The new status ('todo', 'doing', 'done')
        description (str, optional): The new description for the task
    
    Returns:
        bool: True if update was successful, False otherwise
    """
    if title is not None and (not title or not title.strip()):
        return False
    
    # Validate status if provided
    if status is not None:
        valid_statuses = ['todo', 'doing', 'done']
        if status not in valid_statuses:
            return False
    
    try:
        with sqlite3.connect(get_db_path()) as conn:
            cursor = conn.cursor()
            
            # Build dynamic UPDATE query based on provided fields
            updates = []
            params = []
            
            if title is not None:
                updates.append("title = ?")
                params.append(title.strip())
            
            if status is not None:
                updates.append("status = ?")
                params.append(status)
            
            if description is not None:
                updates.append("description = ?")
                params.append(description.strip())
            
            if not updates:
                return False
            
            params.append(task_id)
            query = f"UPDATE todos SET {', '.join(updates)} WHERE id = ?"
            
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error editing task: {e}")
        return False

def change_task_status(task_id, new_status):
    """
    Change the status of a task.
    
    Args:
        task_id (int): The ID of the task
        new_status (str): The new status ('todo', 'doing', 'done')
    
    Returns:
        bool: True if update was successful, False otherwise
    """
    return edit_task(task_id, status=new_status)