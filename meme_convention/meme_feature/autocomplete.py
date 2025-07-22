from meme_convention.db.postgresql.user import User
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
        self.root = None

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
        try:
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
        except ValueError as e:
            print(f"Context category selection cancelled: {e}")
            return None
        except Exception as e:
            print(f"Autocomplete error: {e}")
            return None

    def display_meme_gui(self, context):
        """GUI for displaying memes - modified for better cleanup"""
        # Ensure any existing window is closed first
        if self.root:
            try:
                self.root.destroy()
            except:
                pass

        self.root = tk.Toplevel()
        self.root.title("Select your meme!")

        # Make window appear on top and grab focus
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.focus_force()

        label = tk.Label(self.root)
        label.pack()

        gui = MemeSelectionGUI(self.root, label, None, context, self.user_db.get_random_meme)
        gui.autocomplete_ref = self

        # Create buttons
        btn_accept = tk.Button(self.root, text="Accept (Ctrl + c | Cmd + c)", command=gui.accept)
        btn_accept.pack(side="left", padx=10, pady=10)

        btn_reject = tk.Button(self.root, text="Next Meme(Up down key)", command=gui.reject)
        btn_reject.pack(side="left", padx=10, pady=10)

        btn_quit = tk.Button(self.root, text="Exit (esc)", command=self.quit_and_cleanup)
        btn_quit.pack(side="left", padx=10, pady=10)

        # Bind keyboard shortcuts
        self.root.bind('<Control-c>', gui.accept)
        self.root.bind('<Command-c>', gui.accept)
        self.root.bind('<Up>', gui.reject)
        self.root.bind('<Down>', gui.reject)
        self.root.bind('<Escape>', self.quit_and_cleanup)

        # Handle window close button
        self.root.protocol("WM_DELETE_WINDOW", self.quit_and_cleanup)

        # TODO: mainloop is necessary? When I run the autocomplete function, it will block the main thread.
        self.root.mainloop()

        return self.accepted_image if self.accepted_image else None

    # TODO: In the future, this will be a multimodal and text recording classification.
    # TODO: color doesn't work in the button.
    def quit_and_cleanup(self, event=None):
        """Properly cleanup and close the window"""
        if self.root:
            self.root.quit()  # Exit mainloop
            self.root.destroy()  # Destroy window
            self.root = None

    def classify_context_category(self, categories: list[str]) -> str:
        """Context category classification with better error handling"""
        print(f"🔍 Attempting to classify context with categories: {categories}")

        try:
            # Add debug info about threading context
            import threading
            current_thread = threading.current_thread()
            is_main_thread = current_thread is threading.main_thread()
            print(f"📍 Running on {'main' if is_main_thread else 'background'} thread: {current_thread.name}")

            choice = ContextCategoryDialog.ask(categories)
            print(f"✅ User selected: {choice}")

            if choice is None:
                print("❌ User cancelled context category selection")
                raise ValueError("Context category selection was cancelled by user")

            return choice

        except Exception as e:
            print(f"💥 Error in classify_context_category: {e}")
            print(f"📋 Available categories were: {categories}")
            raise
