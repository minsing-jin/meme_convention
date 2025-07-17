from meme_convention.db.user import User
from meme_convention.frontend.meme_selection import *
import tkinter as tk
from meme_convention.frontend.context_dialog import ContextCategoryDialog


# TODO: Add hot key condition that will trigger recommend and the autocomplete function
class AutoComplete:
    def __init__(self, analysis_model, text, page_image):
        self.user_db = User()
        self.analysis_model = analysis_model
        self.text_context = text
        self.page_image_context = page_image
        self.accepted_image = None

    def autocomplete(self, context_category_lst):
        """
        # TODO: I have to implement the autocomplete function in the future. This issue will be implemented in issue #16.
        1. Implement the gui and autoCopy functionality for the autocomplete.
        2. Autocomplete the multimodal based on the model and context category in the future.
        3. Autocomplete in user's text box and page image context.
        """

        # TODO: Analyze the text and image to determine the context category
        # context = self.classify_context_category(self.text, self.page_image)

        # For now, we will just return the first context category from the list
        context = self.classify_context_category(context_category_lst)
        accepted_image = self.display_meme_gui(context)
        if accepted_image:
            print("User accepted an image!")
            print(accepted_image)
            # Process the accepted image as needed
            return accepted_image
        else:
            print("User didn't accept any image")
            return None

    def display_meme_gui(self, context):
        """GUI for displaying memes and accepting/rejecting them."""
        root = tk.Tk()
        root.title("Select your optimal meme!")
        label = tk.Label(root)
        label.pack()

        gui = MemeSelectionGUI(root, label, None, context, self.user_db.get_random_meme)
        gui.autocomplete_ref = self

        btn_accept = tk.Button(root, text="Accept (Ctrl + c | Cmd + c)", command=gui.accept)
        btn_accept.pack(side="left", padx=10, pady=10)

        btn_reject = tk.Button(root, text="Next Meme(Up down key)", command=gui.reject)
        btn_reject.pack(side="left", padx=10, pady=10)

        btn_quit = tk.Button(root, text="Exit (esc)", command=gui.quit_app)
        btn_quit.pack(side="left", padx=10, pady=10)

        root.bind('<Control-c>', gui.accept)
        root.bind('<Command-c>', gui.accept)
        root.bind('<Up>', gui.reject)
        root.bind('<Down>', gui.reject)
        root.bind('<Escape>', gui.quit_app)

        root.mainloop()

        if self.accepted_image:
            return self.accepted_image
        else:
            print("No image accepted.")
            return None

    # TODO: In the future, this will be a multimodal and text recording classification.
    # TODO: color doesn't work in the button.
    def classify_context_category(self, categories: list[str]) -> str:
        """
        Delegates to a tiny dialog class; keeps old API/exception.
        """
        choice = ContextCategoryDialog.ask(categories)
        if choice is None:
            raise ValueError("Context category selection was cancelled by user")
        return choice