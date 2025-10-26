"""
GUI Module for Todo App
Modern Tkinter interface that uses the existing SQLite helper functions.
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
        self.root.title("Task Manager")
        self.root.geometry("900x650")
        self.root.minsize(800, 600)
        
        # Modern color scheme
        self.colors = {
            'bg': '#f5f6fa',
            'sidebar': '#2c3e50',
            'accent': '#3498db',
            'accent_hover': '#2980b9',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'text_dark': '#2c3e50',
            'text_light': '#ecf0f1',
            'card': '#ffffff',
            'border': '#dfe6e9'
        }
        
        # Configure root background
        self.root.configure(bg=self.colors['bg'])
        
        # Initialize database
        init_database()
        
        # Configure styles
        self.setup_styles()
        
        # Create main container
        main_container = tk.Frame(root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar
        self.setup_sidebar(main_container)
        
        # Create main content area
        content_frame = tk.Frame(main_container, bg=self.colors['bg'])
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.setup_header(content_frame)
        
        # Task list card
        self.setup_task_list(content_frame)
        
        # Status bar
        self.setup_status_bar(content_frame)
        
        # Load initial tasks
        self.refresh_tasks()
    
    def setup_styles(self):
        """Configure modern ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure Treeview
        style.configure("Modern.Treeview",
                       background=self.colors['card'],
                       foreground=self.colors['text_dark'],
                       fieldbackground=self.colors['card'],
                       borderwidth=0,
                       font=('Segoe UI', 10))
        style.configure("Modern.Treeview.Heading",
                       background=self.colors['bg'],
                       foreground=self.colors['text_dark'],
                       borderwidth=0,
                       font=('Segoe UI', 10, 'bold'))
        style.map('Modern.Treeview',
                 background=[('selected', self.colors['accent'])],
                 foreground=[('selected', 'white')])
        
        # Configure buttons
        style.configure("Accent.TButton",
                       background=self.colors['accent'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10))
        style.map("Accent.TButton",
                 background=[('active', self.colors['accent_hover'])])
    
    def setup_sidebar(self, parent):
        """Create modern sidebar with action buttons."""
        sidebar = tk.Frame(parent, bg=self.colors['sidebar'], width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # App title in sidebar
        title_frame = tk.Frame(sidebar, bg=self.colors['sidebar'])
        title_frame.pack(pady=30, padx=20)
        
        tk.Label(title_frame, text="📋", font=('Segoe UI', 32),
                bg=self.colors['sidebar'], fg=self.colors['text_light']).pack()
        tk.Label(title_frame, text="Task Manager", font=('Segoe UI', 14, 'bold'),
                bg=self.colors['sidebar'], fg=self.colors['text_light']).pack()
        
        # Action buttons
        button_config = [
            ("➕ Add Task", self.add_task_dialog, self.colors['success']),
            ("👁️ View Details", self.view_task_dialog, self.colors['accent']),
            ("✏️ Edit Task", self.edit_task_dialog, self.colors['accent']),
            ("🔄 Change Status", self.change_status_dialog, self.colors['warning']),
            ("🗑️ Delete Task", self.delete_task_dialog, self.colors['danger']),
            ("🧹 Clear Completed", self.clear_completed_dialog, '#95a5a6')
        ]
        
        for text, command, color in button_config:
            btn = tk.Button(sidebar, text=text, command=command,
                          bg=color, fg='white', font=('Segoe UI', 11),
                          bd=0, padx=20, pady=12, cursor='hand2',
                          activebackground=self._darken_color(color),
                          activeforeground='white', anchor='w')
            btn.pack(fill=tk.X, padx=15, pady=5)
            
            # Hover effects
            btn.bind('<Enter>', lambda e, b=btn, c=color: b.config(bg=self._darken_color(c)))
            btn.bind('<Leave>', lambda e, b=btn, c=color: b.config(bg=c))
    
    def _darken_color(self, color):
        """Darken a hex color by 20%."""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darker = tuple(int(c * 0.8) for c in rgb)
        return f'#{darker[0]:02x}{darker[1]:02x}{darker[2]:02x}'
    
    def setup_header(self, parent):
        """Create header section."""
        header_frame = tk.Frame(parent, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header_frame, text="My Tasks", font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text_dark']).pack(side=tk.LEFT)
        
        # Stats badges
        self.stats_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        self.stats_frame.pack(side=tk.RIGHT)
        
        self.stat_labels = {}
        for status, color in [('todo', self.colors['warning']), 
                             ('doing', self.colors['accent']), 
                             ('done', self.colors['success'])]:
            badge = tk.Frame(self.stats_frame, bg=color, padx=12, pady=6)
            badge.pack(side=tk.LEFT, padx=5)
            
            label = tk.Label(badge, text=f"{status.upper()}: 0", 
                           font=('Segoe UI', 9, 'bold'),
                           bg=color, fg='white')
            label.pack()
            self.stat_labels[status] = label
        
        # Search and filter bar
        filter_frame = tk.Frame(parent, bg=self.colors['bg'])
        filter_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Search box
        search_container = tk.Frame(filter_frame, bg=self.colors['card'],
                                   highlightbackground=self.colors['border'], highlightthickness=1)
        search_container.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        tk.Label(search_container, text="🔍", font=('Segoe UI', 12),
                bg=self.colors['card']).pack(side=tk.LEFT, padx=(10, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.apply_filters())
        search_entry = tk.Entry(search_container, textvariable=self.search_var,
                               font=('Segoe UI', 10), relief=tk.FLAT,
                               bg=self.colors['card'], fg=self.colors['text_dark'])
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, padx=(0, 10))
        
        # Filter dropdown
        tk.Label(filter_frame, text="Filter:", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text_dark']).pack(side=tk.LEFT, padx=(0, 5))
        
        self.filter_var = tk.StringVar(value="all")
        filter_options = [("All", "all"), ("⏳ Todo", "todo"), ("🔄 Doing", "doing"), ("✅ Done", "done")]
        
        for text, value in filter_options:
            rb = tk.Radiobutton(filter_frame, text=text, variable=self.filter_var, value=value,
                               font=('Segoe UI', 9), bg=self.colors['bg'],
                               selectcolor=self.colors['bg'], activebackground=self.colors['bg'],
                               cursor='hand2', command=self.apply_filters)
            rb.pack(side=tk.LEFT, padx=5)
    
    def setup_task_list(self, parent):
        """Set up the task list display using Treeview."""
        # Card container for task list
        card = tk.Frame(parent, bg=self.colors['card'], relief=tk.FLAT)
        card.pack(fill=tk.BOTH, expand=True)
        
        # Add subtle shadow effect with border
        card.configure(highlightbackground=self.colors['border'], 
                      highlightthickness=1)
        
        # Inner padding
        inner_frame = tk.Frame(card, bg=self.colors['card'])
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Create Treeview with columns
        columns = ("ID", "Title", "Status", "Description")
        self.task_tree = ttk.Treeview(inner_frame, columns=columns, show="headings", 
                                     height=15, style="Modern.Treeview")
        
        # Define column headers and widths
        self.task_tree.heading("ID", text="ID")
        self.task_tree.heading("Title", text="Task Title")
        self.task_tree.heading("Status", text="Status")
        self.task_tree.heading("Description", text="Description")
        
        self.task_tree.column("ID", width=60, minwidth=60, anchor='center')
        self.task_tree.column("Title", width=220, minwidth=150)
        self.task_tree.column("Status", width=100, minwidth=80, anchor='center')
        self.task_tree.column("Description", width=300, minwidth=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(inner_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add row striping effect
        self.task_tree.tag_configure('oddrow', background='#f8f9fa')
        self.task_tree.tag_configure('evenrow', background='#ffffff')
        self.task_tree.tag_configure('todo', foreground=self.colors['warning'])
        self.task_tree.tag_configure('doing', foreground=self.colors['accent'])
        self.task_tree.tag_configure('done', foreground=self.colors['success'])
        
        # Bind double-click to view details
        self.task_tree.bind('<Double-Button-1>', lambda e: self.view_task_dialog())
    
    def setup_status_bar(self, parent):
        """Create modern status bar."""
        status_frame = tk.Frame(parent, bg=self.colors['card'], 
                               highlightbackground=self.colors['border'],
                               highlightthickness=1)
        status_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.status_var = tk.StringVar()
        status_label = tk.Label(status_frame, textvariable=self.status_var,
                               font=('Segoe UI', 9), bg=self.colors['card'],
                               fg=self.colors['text_dark'], anchor='w', padx=15, pady=8)
        status_label.pack(fill=tk.X)
    
    def refresh_tasks(self):
        """Reload tasks from database and update the display."""
        # Load all tasks from database
        self.all_tasks = load_tasks()
        
        # Apply current filters
        self.apply_filters()
        
        # Update status bar and badges with all tasks
        total_tasks = len(self.all_tasks)
        todo_tasks = sum(1 for task in self.all_tasks if task["status"] == "todo")
        doing_tasks = sum(1 for task in self.all_tasks if task["status"] == "doing")
        done_tasks = sum(1 for task in self.all_tasks if task["status"] == "done")
        
        self.status_var.set(f"📊 Total Tasks: {total_tasks}  |  Completed: {done_tasks}/{total_tasks}")
        
        # Update header badges
        self.stat_labels['todo'].config(text=f"TODO: {todo_tasks}")
        self.stat_labels['doing'].config(text=f"DOING: {doing_tasks}")
        self.stat_labels['done'].config(text=f"DONE: {done_tasks}")
    
    def apply_filters(self):
        """Apply search and status filters to the task list."""
        # Clear existing items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Get filter values
        search_text = self.search_var.get().lower() if hasattr(self, 'search_var') else ""
        status_filter = self.filter_var.get() if hasattr(self, 'filter_var') else "all"
        
        # Filter tasks
        filtered_tasks = self.all_tasks if hasattr(self, 'all_tasks') else load_tasks()
        
        # Apply status filter
        if status_filter != "all":
            filtered_tasks = [t for t in filtered_tasks if t["status"] == status_filter]
        
        # Apply search filter
        if search_text:
            filtered_tasks = [t for t in filtered_tasks 
                            if search_text in t["title"].lower() 
                            or search_text in t["description"].lower()]
        
        # Add filtered tasks to treeview
        for idx, task in enumerate(filtered_tasks):
            status_display = task["status"].upper()
            status_emoji = {'TODO': '⏳', 'DOING': '🔄', 'DONE': '✅'}
            status_text = f"{status_emoji.get(status_display, '')} {status_display}"
            
            desc_preview = task["description"][:60] + "..." if len(task["description"]) > 60 else task["description"]
            
            row_tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            status_tag = task["status"]
            
            self.task_tree.insert("", tk.END, 
                                values=(task["id"], task["title"], status_text, desc_preview),
                                tags=(row_tag, status_tag))
    
    def get_selected_task_id(self):
        """Get the ID of the currently selected task."""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a task first.")
            return None
        
        item = self.task_tree.item(selection[0])
        return int(item["values"][0])  # First column is the ID
    
    def add_task_dialog(self):
        """Show modern dialog to add a new task."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Task")
        dialog.geometry("550x500")
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Main container
        container = tk.Frame(dialog, bg=self.colors['bg'])
        container.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Header
        tk.Label(container, text="➕ Create New Task", font=('Segoe UI', 16, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 20))
        
        # Title
        tk.Label(container, text="Task Title", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 5))
        title_entry = tk.Entry(container, font=('Segoe UI', 11), relief=tk.FLAT,
                              bg=self.colors['card'], fg=self.colors['text_dark'],
                              highlightbackground=self.colors['border'], highlightthickness=1)
        title_entry.pack(fill=tk.X, ipady=8, pady=(0, 15))
        title_entry.focus()
        
        # Status
        tk.Label(container, text="Status", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 10))
        status_var = tk.StringVar(value="todo")
        status_frame = tk.Frame(container, bg=self.colors['bg'])
        status_frame.pack(anchor='w', pady=(0, 15))
        
        for val, text, color in [('todo', '⏳ Todo', self.colors['warning']),
                                 ('doing', '🔄 Doing', self.colors['accent']),
                                 ('done', '✅ Done', self.colors['success'])]:
            rb = tk.Radiobutton(status_frame, text=text, variable=status_var, value=val,
                               font=('Segoe UI', 10), bg=self.colors['bg'], fg=color,
                               selectcolor=self.colors['bg'], activebackground=self.colors['bg'],
                               activeforeground=color, cursor='hand2')
            rb.pack(side=tk.LEFT, padx=(0, 15))
        
        # Description
        tk.Label(container, text="Description", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 5))
        desc_text = tk.Text(container, font=('Segoe UI', 10), relief=tk.FLAT,
                           bg=self.colors['card'], fg=self.colors['text_dark'],
                           highlightbackground=self.colors['border'], highlightthickness=1,
                           height=7, wrap=tk.WORD)
        desc_text.pack(fill=tk.X, pady=(0, 15))
        
        # Buttons
        button_frame = tk.Frame(container, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X)
        
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
                messagebox.showinfo("Success", f"✅ Task added successfully!")
            else:
                messagebox.showerror("Error", "Failed to add task.")
        
        cancel_btn = tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                              bg=self.colors['border'], fg=self.colors['text_dark'],
                              font=('Segoe UI', 11), bd=0, padx=25, pady=10, cursor='hand2',
                              activebackground=self._darken_color(self.colors['border']))
        cancel_btn.pack(side=tk.LEFT)
        
        save_btn = tk.Button(button_frame, text="✅ Create Task", command=save_task,
                            bg=self.colors['success'], fg='white', font=('Segoe UI', 11, 'bold'),
                            bd=0, padx=30, pady=12, cursor='hand2',
                            activebackground=self._darken_color(self.colors['success']))
        save_btn.pack(side=tk.RIGHT)
    
    def edit_task_dialog(self):
        """Show modern dialog to edit the selected task."""
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
        dialog.geometry("550x500")
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Main container
        container = tk.Frame(dialog, bg=self.colors['bg'])
        container.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Header
        tk.Label(container, text="✏️ Edit Task", font=('Segoe UI', 16, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 20))
        
        # Title
        tk.Label(container, text="Task Title", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 5))
        title_entry = tk.Entry(container, font=('Segoe UI', 11), relief=tk.FLAT,
                              bg=self.colors['card'], fg=self.colors['text_dark'],
                              highlightbackground=self.colors['border'], highlightthickness=1)
        title_entry.insert(0, current_task["title"])
        title_entry.pack(fill=tk.X, ipady=8, pady=(0, 15))
        title_entry.focus()
        
        # Status
        tk.Label(container, text="Status", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 10))
        status_var = tk.StringVar(value=current_task["status"])
        status_frame = tk.Frame(container, bg=self.colors['bg'])
        status_frame.pack(anchor='w', pady=(0, 15))
        
        for val, text, color in [('todo', '⏳ Todo', self.colors['warning']),
                                 ('doing', '🔄 Doing', self.colors['accent']),
                                 ('done', '✅ Done', self.colors['success'])]:
            rb = tk.Radiobutton(status_frame, text=text, variable=status_var, value=val,
                               font=('Segoe UI', 10), bg=self.colors['bg'], fg=color,
                               selectcolor=self.colors['bg'], activebackground=self.colors['bg'],
                               activeforeground=color, cursor='hand2')
            rb.pack(side=tk.LEFT, padx=(0, 15))
        
        # Description
        tk.Label(container, text="Description", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 5))
        desc_text = tk.Text(container, font=('Segoe UI', 10), relief=tk.FLAT,
                           bg=self.colors['card'], fg=self.colors['text_dark'],
                           highlightbackground=self.colors['border'], highlightthickness=1,
                           height=7, wrap=tk.WORD)
        desc_text.insert("1.0", current_task["description"])
        desc_text.pack(fill=tk.X, pady=(0, 15))
        
        # Buttons
        button_frame = tk.Frame(container, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X)
        
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
                messagebox.showinfo("Success", "✅ Task updated successfully!")
            else:
                messagebox.showerror("Error", "Failed to update task.")
        
        cancel_btn = tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                              bg=self.colors['border'], fg=self.colors['text_dark'],
                              font=('Segoe UI', 11), bd=0, padx=25, pady=10, cursor='hand2',
                              activebackground=self._darken_color(self.colors['border']))
        cancel_btn.pack(side=tk.LEFT)
        
        save_btn = tk.Button(button_frame, text="✅ Apply Changes", command=save_changes,
                            bg=self.colors['accent'], fg='white', font=('Segoe UI', 11, 'bold'),
                            bd=0, padx=30, pady=12, cursor='hand2',
                            activebackground=self._darken_color(self.colors['accent']))
        save_btn.pack(side=tk.RIGHT)
    
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
        
        # Create modern dialog for status change
        dialog = tk.Toplevel(self.root)
        dialog.title("Change Status")
        dialog.geometry("450x400")
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Main container
        container = tk.Frame(dialog, bg=self.colors['bg'])
        container.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Header
        tk.Label(container, text="🔄 Change Task Status", font=('Segoe UI', 16, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 10))
        
        # Task title display
        task_card = tk.Frame(container, bg=self.colors['card'], 
                            highlightbackground=self.colors['border'], highlightthickness=1)
        task_card.pack(fill=tk.X, pady=(0, 20))
        tk.Label(task_card, text=current_task['title'], font=('Segoe UI', 11),
                bg=self.colors['card'], fg=self.colors['text_dark'],
                wraplength=380, justify='left').pack(padx=15, pady=12)
        
        # Status selection
        tk.Label(container, text="Select new status:", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 10))
        
        # Create scrollable frame for status options
        scroll_container = tk.Frame(container, bg=self.colors['bg'])
        scroll_container.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(scroll_container, bg=self.colors['bg'], highlightthickness=0, height=150)
        scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add status options to scrollable frame
        status_var = tk.StringVar(value=current_task["status"])
        
        for val, text, color in [('todo', '⏳ Todo', self.colors['warning']),
                                 ('doing', '🔄 Doing', self.colors['accent']),
                                 ('done', '✅ Done', self.colors['success'])]:
            rb_frame = tk.Frame(scrollable_frame, bg=self.colors['card'],
                               highlightbackground=self.colors['border'], highlightthickness=1)
            rb_frame.pack(fill=tk.X, pady=4, padx=2)
            
            rb = tk.Radiobutton(rb_frame, text=text, variable=status_var, value=val,
                               font=('Segoe UI', 11), bg=self.colors['card'], fg=color,
                               selectcolor=self.colors['card'], activebackground=self.colors['card'],
                               activeforeground=color, cursor='hand2', anchor='w')
            rb.pack(fill=tk.X, padx=15, pady=10)
        
        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Buttons
        button_frame = tk.Frame(container, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        def save_status():
            new_status = status_var.get()
            if change_task_status(task_id, new_status):
                self.refresh_tasks()
                dialog.destroy()
                messagebox.showinfo("Success", "✅ Status updated!")
            else:
                messagebox.showerror("Error", "Failed to update status.")
        
        cancel_btn = tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                              bg=self.colors['border'], fg=self.colors['text_dark'],
                              font=('Segoe UI', 11), bd=0, padx=25, pady=10, cursor='hand2',
                              activebackground=self._darken_color(self.colors['border']))
        cancel_btn.pack(side=tk.LEFT)
        
        save_btn = tk.Button(button_frame, text="✅ Apply Status", command=save_status,
                            bg=self.colors['warning'], fg='white', font=('Segoe UI', 11, 'bold'),
                            bd=0, padx=30, pady=12, cursor='hand2',
                            activebackground=self._darken_color(self.colors['warning']))
        save_btn.pack(side=tk.RIGHT)
    
    def view_task_dialog(self):
        """Show full task details in a read-only dialog."""
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
        dialog.title("Task Details")
        dialog.geometry("550x500")
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Main container
        container = tk.Frame(dialog, bg=self.colors['bg'])
        container.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Header
        tk.Label(container, text="👁️ Task Details", font=('Segoe UI', 16, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 20))
        
        # Task ID
        id_frame = tk.Frame(container, bg=self.colors['card'],
                           highlightbackground=self.colors['border'], highlightthickness=1)
        id_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(id_frame, text=f"ID: {current_task['id']}", font=('Segoe UI', 10),
                bg=self.colors['card'], fg=self.colors['text_dark']).pack(anchor='w', padx=15, pady=8)
        
        # Title
        tk.Label(container, text="Task Title", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 5))
        title_frame = tk.Frame(container, bg=self.colors['card'],
                              highlightbackground=self.colors['border'], highlightthickness=1)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        tk.Label(title_frame, text=current_task["title"], font=('Segoe UI', 11),
                bg=self.colors['card'], fg=self.colors['text_dark'],
                wraplength=480, justify='left').pack(anchor='w', padx=15, pady=12)
        
        # Status
        tk.Label(container, text="Status", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 5))
        status_frame = tk.Frame(container, bg=self.colors['card'],
                               highlightbackground=self.colors['border'], highlightthickness=1)
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        status_colors = {'todo': self.colors['warning'], 'doing': self.colors['accent'], 'done': self.colors['success']}
        status_emoji = {'todo': '⏳', 'doing': '🔄', 'done': '✅'}
        status_text = f"{status_emoji[current_task['status']]} {current_task['status'].upper()}"
        
        tk.Label(status_frame, text=status_text, font=('Segoe UI', 11, 'bold'),
                bg=self.colors['card'], fg=status_colors[current_task['status']]).pack(anchor='w', padx=15, pady=12)
        
        # Description
        tk.Label(container, text="Description", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text_dark']).pack(anchor='w', pady=(0, 5))
        desc_frame = tk.Frame(container, bg=self.colors['card'],
                             highlightbackground=self.colors['border'], highlightthickness=1)
        desc_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        desc_text = tk.Text(desc_frame, font=('Segoe UI', 10), relief=tk.FLAT,
                           bg=self.colors['card'], fg=self.colors['text_dark'],
                           height=8, wrap=tk.WORD, state=tk.NORMAL)
        desc_text.insert("1.0", current_task["description"] if current_task["description"] else "(No description)")
        desc_text.config(state=tk.DISABLED)
        desc_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Close button
        close_btn = tk.Button(container, text="Close", command=dialog.destroy,
                             bg=self.colors['accent'], fg='white', font=('Segoe UI', 11),
                             bd=0, padx=30, pady=12, cursor='hand2',
                             activebackground=self._darken_color(self.colors['accent']))
        close_btn.pack(pady=(10, 0))
    
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
        """Clear all completed tasks with confirmation."""
        # Count completed tasks
        tasks = load_tasks()
        completed_count = sum(1 for task in tasks if task["status"] == "done")
        
        if completed_count == 0:
            messagebox.showinfo("No Completed Tasks", "There are no completed tasks to clear.")
            return
        
        result = messagebox.askyesno("Confirm Clear Completed", 
                                   f"Are you sure you want to delete all {completed_count} completed task(s)?")
        
        if result:
            deleted_count = clear_completed_tasks()
            if deleted_count > 0:
                self.refresh_tasks()
                messagebox.showinfo("Success", f"✅ Cleared {deleted_count} completed task(s).")
            else:
                messagebox.showerror("Error", "Failed to clear completed tasks.")


def run_gui():
    """Create and run the GUI application."""
    root = tk.Tk()
    app = TodoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()