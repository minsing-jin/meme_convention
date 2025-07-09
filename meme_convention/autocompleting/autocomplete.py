from meme_convention.db.user import User
from tkinter import messagebox
from PIL import Image, ImageTk
from utils.gui import *
import pyperclipimg as pci
import tkinter as tk
import io


# TODO: Add hot key condition that will trigger recommend and the autocomplete function
class AutoComplete:
    def __init__(self, analysis_model, text, page_image):
        self.user_db = User()
        self.analysis_model = analysis_model
        self.text_context = text
        self.page_image_context = page_image

    def autocomplete(self, user_choice, context_category_lst):
        """
        # TODO: Autocomplete the multimodal based on the model and context category in the future.
        """

        # TODO: Analyze the text and image to determine the context category
        # context = self.classify_context_category(self.text, self.page_image)

        # For now, we will just return the first context category from the list
        context = self.classify_context_category(user_choice, context_category_lst)
        meme = self.gui_display_meme(context)
        meme = Image.open(io.BytesIO(bytes(meme[-1])))
        return meme

    def gui_display_meme(self, context):
        """GUI for displaying memes and accepting/rejecting them."""
        root = tk.Tk()
        root.title("Meme Viewer")
        label = tk.Label(root)
        label.pack()

        meme = self.user_db.get_random_meme(context)
        meme_img = Image.open(io.BytesIO(bytes(meme[-1])))

        btn_accept = tk.Button(root, text="Accept (Copy)", command=accept(root, meme_img))
        btn_accept.pack(side="left", padx=10, pady=10)

        btn_reject = tk.Button(root, text="Reject (Next Meme)", command=reject(label, meme_img))
        btn_reject.pack(side="left", padx=10, pady=10)

        btn_quit = tk.Button(root, text="Exit", command=quit_app(root))
        btn_quit.pack(side="left", padx=10, pady=10)

        root.bind('<Control-c>', accept)
        root.bind('<Up>', reject)
        root.bind('<Down>', reject)
        root.bind('<Escape>', quit_app)

        root.mainloop()
        return meme

    # TODO: This method will be implemented after released of the first version
    def classify_context_category(self, user_choice, context_category_lst):
        """
        Classify and analyze the context category based on the text and page.
        """
        # TODO: Autocomplete the multimodal based on the model and context category in the future.
        # context = self.analysis_model.analyze(self.text, self.page_image, context_category=context_category_lst)

        # For now, we will just return the user choice if it is valid
        user_choice = user_choice.lower()
        if user_choice in context_category_lst:
            return user_choice
        else:
            raise ValueError(f"Invalid context category: {user_choice}. "
                             f"Available categories: {', '.join(context_category_lst)}")
