import sqlite3

conn = sqlite3.connect('data/todo.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables in database:", tables)

if tables:
    cursor.execute("SELECT * FROM todos")
    rows = cursor.fetchall()
    print(f"Number of rows in todos: {len(rows)}")
    
conn.close()
