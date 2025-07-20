from pynput import keyboard
import threading
import queue
import time
import tkinter as tk


class MainThreadExecutor:
    def __init__(self):
        self.task_queue = queue.Queue()
        self.running = True
        self.root = None
        self.gui_active = False

    def add_task(self, func, *args, **kwargs):
        """Add a task to be executed on the main thread"""
        self.task_queue.put((func, args, kwargs))

    def process_tasks(self):
        """Process tasks on the main thread with GUI awareness"""
        try:
            while not self.task_queue.empty():
                func, args, kwargs = self.task_queue.get_nowait()

                # Check if this is a GUI-related task
                if 'autocomplete' in func.__name__.lower():
                    self.gui_active = True

                func(*args, **kwargs)
                self.task_queue.task_done()
        except queue.Empty:
            pass

        # Adjust processing frequency based on GUI state
        if self.running and self.root:
            interval = 50 if self.gui_active else 10
            self.root.after(interval, self.process_tasks)

    def create_main_window(self):
        """Create a hidden main window for task processing"""
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.after(1, self.process_tasks)

    def run_main_loop(self):
        """Run the main tkinter loop"""
        self.create_main_window()
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Main loop error: {e}")
        finally:
            self.running = False
