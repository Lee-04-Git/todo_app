#!/usr/bin/env python3
"""
Todo App - Main Entry Point
Launches the Tkinter GUI application.
"""

from gui import run_gui
from utils.save_helper import init_database

def main():
    """Main function to run the todo application."""
    # Initialize database first
    init_database()
    
    # Launch GUI
    run_gui()

if __name__ == "__main__":
    main()