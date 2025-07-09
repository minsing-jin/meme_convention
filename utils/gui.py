import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pyperclipimg as pci
import io

def show_image(label, img):
    photo = ImageTk.PhotoImage(img)
    label.config(image=photo)
    label.image = photo

def accept(root, img):
    # TODO: check the right image format for copying to clipboard
    pci.copy(img)
    messagebox.showinfo("Copied", "Image copied to clipboard!")
    root.destroy()

def reject(label, img):
    show_image(label, img)

def quit_app(root):
    root.destroy()
