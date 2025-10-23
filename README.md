# Todo App

A simple command-line todo application written in Python.

## Features

- Add new tasks
- Edit existing tasks
- Delete tasks
- Mark tasks as complete/incomplete
- Persistent storage using JSON

## Structure

```
todo_app/
│
├── main.py                # Entry point — runs the app
│
├── data/
│   └── todos.json         # Stores to-do items
│
├── utils/
│   ├── __init__.py        # Makes utils a Python package
│   ├── add_helper.py      # Handles adding tasks
│   ├── edit_helper.py     # Handles editing tasks
│   ├── delete_helper.py   # Handles deleting tasks
│   └── save_helper.py     # Handles saving/loading tasks
│
└── README.md              # This file
```

## How to Run

1. Navigate to the todo_app directory
2. Run the application:
   ```bash
   python main.py
   ```

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses only standard library)

## Usage

The application will provide a menu-driven interface to manage your tasks. Tasks are automatically saved to `data/todos.json` and will persist between sessions.