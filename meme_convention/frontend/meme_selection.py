import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from meme_convention.frontend.image_processor import GIFProcessor, GIFAnimator
import pyperclipimg as pci
import pyperclip
import io
import os


# TODO: copy gif meme image to clipboard
class MemeSelectionGUI:
    def __init__(self, root, label, img, context, get_image_func, autocomplete_ref=None):
        self.root = root
        self.label = label
        self.meme_img = img
        self.meme_io = None
        self.context = context
        self.get_image_func = get_image_func
        self.autocomplete_ref = autocomplete_ref
        self.gif_animator = None  # Replace anim_id with gif_animator

        self.show_image()

    def show_image(self, event=None):
        # Stop previous animation if running
        if self.gif_animator is not None:
            self.gif_animator.stop_animation()
            self.gif_animator = None

        meme = self.get_image_func(self.context)
        self.meme_io = io.BytesIO(meme)
        self.meme_img = Image.open(self.meme_io)

        if getattr(self.meme_img, "is_animated", False):
            # Create and start GIF animator
            self.gif_animator = GIFAnimator(self.meme_img, self.label)
            self.gif_animator.start_animation()
        else:
            photo = ImageTk.PhotoImage(self.meme_img)
            self.label.config(image=photo)
            self.label.image = photo

    def accept(self, event=None):
        try:
            # Check if the image is animated (GIF)
            if getattr(self.meme_img, "is_animated", False):
                gif_processor = GIFProcessor()
                gif_processor.send_gif_to_clipboard(self.root, self.meme_io)
            else:
                # For static images, use your existing pyperclipimg method
                pci.copy(self.meme_img)

            # Store the accepted image in autocomplete instance
            if self.autocomplete_ref:
                self.autocomplete_ref.accepted_image = self.meme_img

            AutoCloseMessageBox(
                self.root,
                "Copied",
                f"GIF Meme Copied" if getattr(self.meme_img, "is_animated", False) else "Image Meme Copied",
                timeout=2000
            )
            self.root.after(2100, self.root.destroy)
            return self.meme_img
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy: {str(e)}")

    def reject(self, event=None):
        self.show_image()

    def quit_app(self, event=None):
        # Clean up animation before closing
        if self.gif_animator is not None:
            self.gif_animator.stop_animation()
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
