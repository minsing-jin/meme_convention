# meme_convention/utils/gui.py
import tkinter as tk

def center_window(win: tk.Misc, w: int | None = None, h: int | None = None) -> None:
    """Center *already-sized* window or given (w,h) on screen."""
    win.update_idletasks()
    width  = w or win.winfo_width()
    height = h or win.winfo_height()
    x = (win.winfo_screenwidth()  // 2) - (width  // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")
