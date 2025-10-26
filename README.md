# Task Manager App

A modern task management application with a Tkinter GUI and SQLite database backend.

## Features

### Full CRUD Operations
- ✅ **Create** - Add new tasks with title, status, and description
- ✅ **Read** - View all tasks with search and filter capabilities
- ✅ **Update** - Edit task details and change status
- ✅ **Delete** - Remove individual tasks or bulk delete completed tasks

### User Interface
- Modern, clean GUI with color-coded task statuses
- Real-time search functionality
- Filter tasks by status (Todo, Doing, Done)
- View full task details with double-click
- Quick status change dialog
- Bulk operations (clear all completed tasks)
- Task statistics dashboard

### Data Management
- SQLite database for reliable persistence
- Automatic database initialization
- Support for task descriptions
- Three status levels: Todo, Doing, Done

## Structure

```
task_manager/
│
├── main.py                # Entry point — runs the app
├── gui.py                 # Tkinter GUI interface
│
├── data/
│   └── todo.db            # SQLite database
│
├── utils/
│   ├── add_helper.py      # CREATE - Add new tasks
│   ├── save_helper.py     # READ - Load tasks from database
│   ├── edit_helper.py     # UPDATE - Edit existing tasks
│   └── delete_helper.py   # DELETE - Remove tasks
│
├── queries/               # SQL query reference files
│   ├── create_table.txt
│   ├── insert_task.txt
│   ├── select_all_tasks.txt
│   ├── update_task.txt
│   ├── delete_task.txt
│   └── delete_completed_tasks.txt
│
└── README.md              # This file
```

## How to Run

1. Navigate to the project directory
2. Run the application:
   ```bash
   python main.py
   ```

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses only standard library: tkinter, sqlite3)

## Usage

### Sidebar Actions
- **➕ Add Task** - Create a new task with title, status, and description
- **👁️ View Details** - View full task information (or double-click a task)
- **✏️ Edit Task** - Modify task title, status, or description
- **🔄 Change Status** - Quickly update task status
- **🗑️ Delete Task** - Remove a single task
- **🧹 Clear Completed** - Bulk delete all completed tasks

### Search & Filter
- Use the search box to find tasks by title or description
- Filter by status: All, Todo, Doing, or Done
- Real-time filtering as you type

### Task Statuses
- **⏳ Todo** - Tasks not yet started (yellow)
- **🔄 Doing** - Tasks in progress (blue)
- **✅ Done** - Completed tasks (green)

## Database Schema

```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    status TEXT DEFAULT 'todo',
    description TEXT DEFAULT ''
)
```

Tasks are automatically saved to the SQLite database and persist between sessions.