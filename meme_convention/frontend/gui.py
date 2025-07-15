import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pyperclipimg as pci
import pyperclip
import io
import tempfile
import os

# TODO: copy gif meme image to clipboard
class GUI:
    def __init__(self, root, label, img, context, get_image_func):
        self.root = root
        self.label = label
        self.meme_img = img

        self.test_io = None

        self.context = context
        self.get_image_func = get_image_func
        self.anim_id = None  # Track animation callback

        self.show_image()

    # TODO: solve the issue gif meme image copy issue not png
    def show_image(self, event=None):
        # Stop previous animation if running
        if self.anim_id is not None:
            self.label.after_cancel(self.anim_id)
            self.anim_id = None

        meme = self.get_image_func(self.context)
        self.meme_img = Image.open(io.BytesIO(bytes(meme[-1])))

        self.test_io = io.BytesIO(bytes(meme[-1]))
        print(self.meme_img)
        print("bytes io: ", io.BytesIO(bytes(meme[-1])))

        if getattr(self.meme_img, "is_animated", False):
            self.frames = []
            self.durations = []
            try:
                while True:
                    frame = self.meme_img.copy()
                    self.frames.append(ImageTk.PhotoImage(frame))
                    duration = self.meme_img.info.get('duration', 100)
                    self.durations.append(duration)
                    self.meme_img.seek(self.meme_img.tell() + 1)
            except EOFError:
                pass

            self.current_frame = 0
            self.animate_gif()
        else:
            photo = ImageTk.PhotoImage(self.meme_img)
            self.label.config(image=photo)
            self.label.image = photo

    def animate_gif(self):
        frame = self.frames[self.current_frame]
        self.label.config(image=frame)
        self.label.image = frame
        delay = self.durations[self.current_frame]
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.anim_id = self.label.after(delay, self.animate_gif)

    def accept(self, event=None):
        # TODO: gif image can't copy. So we have to generate link to copy gif.
        pci.copy(self.meme_img)

        AutoCloseMessageBox(
            self.root,
            "Copied",
            f"GIF Copied",
            timeout=2000
        )
        self.root.after(2100, self.root.destroy)
        return self.meme_img

    def reject(self, event=None):
        self.show_image()

    def quit_app(self, event=None):
        self.root.destroy()


class AutoCloseMessageBox(tk.Toplevel):
    def __init__(self, parent, title, message, timeout=2000):
        super().__init__(parent)
        self.title(title)
        self.geometry("340x120")
        self.configure(bg="#2d2d2d", bd=2, relief="ridge")

        # Icon or emoji
        icon_label = tk.Label(self, text="✅", font=("Arial", 32), bg="#2d2d2d", fg="#4caf50")
        icon_label.pack(pady=(18, 0))

        # Message text
        msg_label = tk.Label(
            self,
            text=message,
            font=("Segoe UI", 14, "bold"),
            bg="#2d2d2d",
            fg="#e0e0e0",
            wraplength=300,
            justify="center"
        )
        msg_label.pack(pady=(8, 18), padx=10)

        self.after(timeout, self.destroy)
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)
