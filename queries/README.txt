================================================================================
TODO APP - SQL QUERIES GUIDE
================================================================================

Welcome! This guide explains all SQL queries used in the Todo App.
Each query file shows how we interact with the todo.db database.

================================================================================
WHAT'S IN THE DATABASE?
================================================================================

Table Name: todos

Columns:
  id          → Unique number for each task (automatically assigned)
  title       → The task name (required)
  status      → Where the task is: 'todo', 'doing', or 'done'
  description → Extra details about the task

Example of what the table looks like:

┌────┬──────────────────┬────────┬──────────────────────────┐
│ id │ title            │ status │ description              │
├────┼──────────────────┼────────┼──────────────────────────┤
│ 1  │ Write report     │ done   │ Quarterly sales report   │
│ 2  │ Review code      │ doing  │ Check PR #123            │
│ 3  │ Send email       │ todo   │ Follow up with client    │
│ 4  │ Update database  │ todo   │ Add new fields to schema │
│ 5  │ Test features    │ doing  │ Run integration tests    │
└────┴──────────────────┴────────┴──────────────────────────┘

================================================================================
HOW QUERIES ARE USED (STEP BY STEP)
================================================================================

STEP 0: SETUP
-------------
File: 00_setup_create_table.txt
What it does: Creates the todos table when the app first runs
Code location: utils/save_helper.py - init_database()


STEP 1: CREATE (Add Data)
--------------------------
File: 01_create_insert_task.txt
What it does: Adds a new task to the database
When: User clicks "Add Task" button
Code location: utils/add_helper.py - add_task()


STEP 2: READ (Get Data)
------------------------
File: 02_read_select_all_tasks.txt
What it does: Retrieves all tasks from the database
When: App loads or user refreshes the task list
Code location: utils/save_helper.py - load_tasks()


STEP 3: UPDATE (Change Data)
-----------------------------
File: 03_update_task.txt
What it does: Modifies existing task information
When: User edits a task or changes its status (todo → doing → done)
Code location: utils/edit_helper.py - edit_task(), change_task_status()


STEP 4: DELETE (Remove One Task)
---------------------------------
File: 04_delete_single_task.txt
What it does: Removes a specific task from the database
When: User selects a task and clicks "Delete Task"
Code location: utils/delete_helper.py - delete_task()


STEP 5: DELETE (Remove Multiple Tasks)
---------------------------------------
File: 05_delete_completed_tasks.txt
What it does: Removes all tasks marked as 'done'
When: User clicks "Clear Done" button
Code location: utils/delete_helper.py - clear_completed_tasks()

================================================================================
TYPICAL USER WORKFLOW
================================================================================

1. User opens app
   → App creates table if it doesn't exist (00_setup_create_table.txt)

2. User adds "Write report" task
   → INSERT query runs (01_create_insert_task.txt)

3. App displays all tasks on screen
   → SELECT query runs (02_read_select_all_tasks.txt)

4. User starts working, changes status to "doing"
   → UPDATE query runs (03_update_task.txt)

5. User finishes task, marks as "done"
   → UPDATE query runs (03_update_task.txt)

6. User deletes a specific task
   → DELETE query runs (04_delete_single_task.txt)

7. User clears all completed tasks
   → DELETE query runs (05_delete_completed_tasks.txt)

================================================================================
QUICK REFERENCE
================================================================================

Operation | File                           | User Action
----------|--------------------------------|------------------------
SETUP     | 00_setup_create_table.txt      | App starts
CREATE    | 01_create_insert_task.txt      | Add Task
READ      | 02_read_select_all_tasks.txt   | View tasks
UPDATE    | 03_update_task.txt             | Edit/Change status
DELETE    | 04_delete_single_task.txt      | Delete one task
DELETE    | 05_delete_completed_tasks.txt  | Clear done tasks

================================================================================

================================================================================
TESTING QUERIES IN SQLTOOLS
================================================================================

⚠️ IMPORTANT: Files 00-05 contain ? placeholders used by Python code.
These cannot be run directly in SQLTools.

To test queries manually, see: testing/test_queries.sql
→ This file has real values and is ready to run in SQLTools
→ Includes safe test queries and helpful examples

How to use:
1. Open testing/test_queries.sql
2. Highlight any query
3. Press Ctrl+E Ctrl+E (or right-click → Run Query)
4. View results

================================================================================
