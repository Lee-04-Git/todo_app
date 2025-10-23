SQL QUERIES REFERENCE
=====================

This folder contains all SQL queries used in the Todo App helper functions.
Each file represents a specific database operation.

DATABASE SCHEMA:
----------------
📋 The complete database schema can be found in: create_table.txt

FILE STRUCTURE:
---------------
create_table.txt              - CREATE TABLE query for todos table
insert_task.txt               - INSERT query for adding new tasks
select_all_tasks.txt          - SELECT query for loading all tasks
update_task.txt               - UPDATE query for editing tasks
delete_task.txt               - DELETE query for removing a task
delete_completed_tasks.txt    - DELETE query for clearing done tasks
check_table_exists.txt        - Query to check if table exists
get_table_info.txt            - PRAGMA query to get table structure
drop_table.txt                - DROP TABLE query for migration

PARAMETER PLACEHOLDERS:
-----------------------
? = Placeholder for parameterized queries (prevents SQL injection)

HELPER FUNCTION MAPPING:
------------------------
utils/save_helper.py:
  - create_table.txt
  - select_all_tasks.txt
  - check_table_exists.txt
  - get_table_info.txt
  - drop_table.txt

utils/add_helper.py:
  - insert_task.txt

utils/edit_helper.py:
  - update_task.txt

utils/delete_helper.py:
  - delete_task.txt
  - delete_completed_tasks.txt
