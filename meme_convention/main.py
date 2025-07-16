from pynput import keyboard
from meme_convention.meme_feature.autocomplete import AutoComplete
import threading
import tkinter as tk
import queue


# class MemeApp:
#     def __init__(self):
#         self.hotkey_listener = None
#         self.autocomplete_instance = None
#         self.gui_queue = queue.Queue()
#         self.running = True
#         self.root = None
#         self.setup_hotkeys()
#
#     def setup_hotkeys(self):
#         """Setup global hotkeys for the application"""
#
#         def on_activate():
#             print('Global hotkey activated!')
#             # Queue the GUI display request
#             self.gui_queue.put(("show_meme", "pr"))
#
#         hotkey_combinations = {
#             '<ctrl>+<shift>+m': on_activate,
#         }
#
#         self.hotkey_listener = keyboard.GlobalHotKeys(hotkey_combinations)
#         self.hotkey_listener.start()
#
#     def process_gui_queue(self):
#         """Process GUI display requests from the queue in the main thread"""
#         try:
#             while not self.gui_queue.empty():
#                 command, context = self.gui_queue.get_nowait()
#                 if command == "show_meme" and self.autocomplete_instance:
#                     # This runs in the main thread, so it's safe for GUI operations
#                     self.autocomplete_instance.gui_display_meme(context)
#         except queue.Empty:
#             pass
#
#         # Schedule next check
#         if self.running:
#             self.root.after(100, self.process_gui_queue)
#
#     def stop_hotkeys(self):
#         """Stop the global hotkey listener"""
#         if self.hotkey_listener:
#             self.hotkey_listener.stop()
#
#     def run(self):
#         """Main application loop"""
#         self.root = tk.Tk()
#         self.root.withdraw()  # Hide the main window
#         self.root.title("Meme App Background")
#
#         # Start processing the GUI queue
#         self.process_gui_queue()
#
#         # Set up cleanup
#         self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
#
#         print("Meme app is running. Press Ctrl+Shift+M to show meme GUI.")
#
#         try:
#             self.root.mainloop()
#         except KeyboardInterrupt:
#             self.on_closing()
#
#     def on_closing(self):
#         """Handle application closing"""
#         self.running = False
#         self.stop_hotkeys()
#         if self.root:
#             self.root.destroy()


if __name__ == "__main__":
    # app = MemeApp()
    # app.autocomplete_instance = AutoComplete(None, None, None)
    # app.run()

    autocomplete = AutoComplete(analysis_model=None, text=None, page_image=None)
    autocomplete.gui_display_meme("pr")
