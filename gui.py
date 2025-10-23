"""
GUI Module for Todo App
Simple Tkinter interface that uses the existing SQLite helper functions.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from utils.save_helper import load_tasks, init_database
from utils.add_helper import add_task
from utils.edit_helper import edit_task, change_task_status
from utils.delete_helper import delete_task, clear_completed_tasks


class TodoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo App - SQLite Edition")
        self.root.geometry("600x500")
        
        # Initialize database
        init_database()
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="My Todo List", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Task list (Treeview for better display)
        self.setup_task_list(main_frame)
        
        # Buttons frame
        self.setup_buttons(main_frame)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Load initial tasks
        self.refresh_tasks()
    
    def setup_task_list(self, parent):
        """Set up the task list display using Treeview."""
        # Create Treeview with columns
        columns = ("ID", "Title", "Status", "Description")
        self.task_tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        
        # Define column headers and widths
        self.task_tree.heading("ID", text="ID")
        self.task_tree.heading("Title", text="Title")
        self.task_tree.heading("Status", text="Status")
        self.task_tree.heading("Description", text="Description")
        
        self.task_tree.column("ID", width=50, minwidth=50)
        self.task_tree.column("Title", width=200, minwidth=150)
        self.task_tree.column("Status", width=100, minwidth=80)
        self.task_tree.column("Description", width=250, minwidth=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid the treeview and scrollbar
        self.task_tree.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S))
    
    def setup_buttons(self, parent):
        """Set up the button panel."""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Button styling
        button_width = 12
        
        # Add Task button
        ttk.Button(button_frame, text="Add Task", width=button_width,
                  command=self.add_task_dialog).grid(row=0, column=0, padx=5)
        
        # Edit Task button
        ttk.Button(button_frame, text="Edit Task", width=button_width,
                  command=self.edit_task_dialog).grid(row=0, column=1, padx=5)
        
        # Toggle Complete button
        ttk.Button(button_frame, text="Change Status", width=button_width,
                  command=self.change_status_dialog).grid(row=0, column=2, padx=5)
        
        # Delete Task button
        ttk.Button(button_frame, text="Delete Task", width=button_width,
                  command=self.delete_task_dialog).grid(row=0, column=3, padx=5)
        
        # Clear Completed button
        ttk.Button(button_frame, text="Clear Done", width=button_width,
                  command=self.clear_completed_dialog).grid(row=0, column=4, padx=5)
    
    def refresh_tasks(self):
        """Reload tasks from database and update the display."""
        # Clear existing items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Load tasks from database
        tasks = load_tasks()
        
        # Add tasks to treeview
        for task in tasks:
            status_display = task["status"].upper()
            desc_preview = task["description"][:50] + "..." if len(task["description"]) > 50 else task["description"]
            self.task_tree.insert("", tk.END, values=(task["id"], task["title"], status_display, desc_preview))
        
        # Update status bar
        total_tasks = len(tasks)
        todo_tasks = sum(1 for task in tasks if task["status"] == "todo")
        doing_tasks = sum(1 for task in tasks if task["status"] == "doing")
        done_tasks = sum(1 for task in tasks if task["status"] == "done")
        
        self.status_var.set(f"Total: {total_tasks} | Todo: {todo_tasks} | Doing: {doing_tasks} | Done: {done_tasks}")
    
    def get_selected_task_id(self):
        """Get the ID of the currently selected task."""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a task first.")
            return None
        
        item = self.task_tree.item(selection[0])
        return int(item["values"][0])  # First column is the ID
    
    def add_task_dialog(self):
        """Show dialog to add a new task."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Task")
        dialog.geometry("500x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Title
        ttk.Label(dialog, text="Title:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        title_entry = ttk.Entry(dialog, width=50)
        title_entry.grid(row=0, column=1, padx=10, pady=10)
        title_entry.focus()
        
        # Status
        ttk.Label(dialog, text="Status:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        status_var = tk.StringVar(value="todo")
        status_frame = ttk.Frame(dialog)
        status_frame.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        ttk.Radiobutton(status_frame, text="Todo", variable=status_var, value="todo").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(status_frame, text="Doing", variable=status_var, value="doing").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(status_frame, text="Done", variable=status_var, value="done").pack(side=tk.LEFT, padx=5)
        
        # Description
        ttk.Label(dialog, text="Description:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.NW)
        desc_text = tk.Text(dialog, width=50, height=10)
        desc_text.grid(row=2, column=1, padx=10, pady=10)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        def save_task():
            title = title_entry.get().strip()
            if not title:
                messagebox.showwarning("Empty Title", "Please enter a task title.")
                return
            
            description = desc_text.get("1.0", tk.END).strip()
            status = status_var.get()
            
            task_id = add_task(title, status, description)
            if task_id:
                self.refresh_tasks()
                dialog.destroy()
                messagebox.showinfo("Success", f"Task added with ID: {task_id}")
            else:
                messagebox.showerror("Error", "Failed to add task.")
        
        ttk.Button(button_frame, text="Save", command=save_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def edit_task_dialog(self):
        """Show dialog to edit the selected task."""
        task_id = self.get_selected_task_id()
        if task_id is None:
            return
        
        # Get current task data
        tasks = load_tasks()
        current_task = next((t for t in tasks if t["id"] == task_id), None)
        if not current_task:
            messagebox.showerror("Error", "Task not found.")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Task")
        dialog.geometry("500x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Title
        ttk.Label(dialog, text="Title:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        title_entry = ttk.Entry(dialog, width=50)
        title_entry.insert(0, current_task["title"])
        title_entry.grid(row=0, column=1, padx=10, pady=10)
        title_entry.focus()
        
        # Status
        ttk.Label(dialog, text="Status:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        status_var = tk.StringVar(value=current_task["status"])
        status_frame = ttk.Frame(dialog)
        status_frame.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        ttk.Radiobutton(status_frame, text="Todo", variable=status_var, value="todo").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(status_frame, text="Doing", variable=status_var, value="doing").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(status_frame, text="Done", variable=status_var, value="done").pack(side=tk.LEFT, padx=5)
        
        # Description
        ttk.Label(dialog, text="Description:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.NW)
        desc_text = tk.Text(dialog, width=50, height=10)
        desc_text.insert("1.0", current_task["description"])
        desc_text.grid(row=2, column=1, padx=10, pady=10)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        def save_changes():
            title = title_entry.get().strip()
            if not title:
                messagebox.showwarning("Empty Title", "Please enter a task title.")
                return
            
            description = desc_text.get("1.0", tk.END).strip()
            status = status_var.get()
            
            if edit_task(task_id, title=title, status=status, description=description):
                self.refresh_tasks()
                dialog.destroy()
                messagebox.showinfo("Success", "Task updated successfully.")
            else:
                messagebox.showerror("Error", "Failed to update task.")
        
        ttk.Button(button_frame, text="Save", command=save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def change_status_dialog(self):
        """Change the status of the selected task."""
        task_id = self.get_selected_task_id()
        if task_id is None:
            return
        
        # Get current task
        tasks = load_tasks()
        current_task = next((t for t in tasks if t["id"] == task_id), None)
        if not current_task:
            return
        
        # Create simple dialog for status change
        dialog = tk.Toplevel(self.root)
        dialog.title("Change Task Status")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text=f"Task: {current_task['title']}", font=("Arial", 10, "bold")).pack(pady=10)
        ttk.Label(dialog, text="Select new status:").pack(pady=5)
        
        status_var = tk.StringVar(value=current_task["status"])
        status_frame = ttk.Frame(dialog)
        status_frame.pack(pady=10)
        
        ttk.Radiobutton(status_frame, text="Todo", variable=status_var, value="todo").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(status_frame, text="Doing", variable=status_var, value="doing").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(status_frame, text="Done", variable=status_var, value="done").pack(side=tk.LEFT, padx=10)
        
        def save_status():
            new_status = status_var.get()
            if change_task_status(task_id, new_status):
                self.refresh_tasks()
                dialog.destroy()
                messagebox.showinfo("Success", "Task status updated.")
            else:
                messagebox.showerror("Error", "Failed to update status.")
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Save", command=save_status).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def delete_task_dialog(self):
        """Delete the selected task with confirmation."""
        task_id = self.get_selected_task_id()
        if task_id is None:
            return
        
        # Get task title for confirmation
        selection = self.task_tree.selection()[0]
        task_title = self.task_tree.item(selection)["values"][1]
        
        result = messagebox.askyesno("Confirm Delete", 
                                   f"Are you sure you want to delete this task?\n\n'{task_title}'")
        
        if result:
            if delete_task(task_id):
                self.refresh_tasks()
                messagebox.showinfo("Success", "Task deleted successfully.")
            else:
                messagebox.showerror("Error", "Failed to delete task.")
    
    def clear_completed_dialog(self):
        """Clear all completed (done) tasks with confirmation."""
        result = messagebox.askyesno("Confirm Clear", 
                                   "Are you sure you want to delete all tasks with 'Done' status?")
        
        if result:
            deleted_count = clear_completed_tasks()
            self.refresh_tasks()
            messagebox.showinfo("Success", f"Cleared {deleted_count} completed tasks.")


def run_gui():
    """Create and run the GUI application."""
    root = tk.Tk()
    app = TodoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()