-- ============================================
-- TEST QUERIES - Ready to Run
-- ============================================

-- TEST 1: View all tasks (SAFE - READ ONLY)
SELECT id,
    title,
    status,
    description
FROM todos
ORDER BY id;

-- TEST 2: Insert a new task (CREATES DATA)
INSERT INTO todos (title, status, description)
VALUES ('Test Task 2', 'doing', 'This is a test task take two');

-- TEST 3: Update task status (MODIFIES DATA)
-- Change task ID 1 to 'doing'
UPDATE todos
SET status = 'doing'
WHERE id = 1;

-- TEST 4: Update all fields (MODIFIES DATA)
-- Update task ID 1 completely
UPDATE todos
SET title = 'Updated Task',
    status = 'done',
    description = 'Task has been updated'
WHERE id = 1;

-- TEST 5: Delete a specific task (DELETES DATA)
-- Delete task ID 999 (safe - probably doesn't exist)
DELETE FROM todos
WHERE id = 999;

-- TEST 6: Delete all completed tasks (DELETES DATA)
-- WARNING: This removes all 'done' tasks
DELETE FROM todos
WHERE status = 'done';
-- ============================================
-- SAFE QUERIES TO RUN ANYTIME
-- ============================================
-- Count total tasks
SELECT COUNT(*) as total_tasks
FROM todos;
-- Count by status
SELECT status,
    COUNT(*) as count
FROM todos
GROUP BY status;
-- View only todo tasks
SELECT *
FROM todos
WHERE status = 'todo';
-- View only doing tasks
SELECT *
FROM todos
WHERE status = 'doing';
-- View only done tasks
SELECT *
FROM todos
WHERE status = 'done';
-- Get the most recent task
SELECT *
FROM todos
ORDER BY id DESC
LIMIT 1;