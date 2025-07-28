import os
import random
from pathlib import Path

LOCALDB_PATH = os.path.join(Path("./").parent, 'resources', 'local_db')

class LocalDB:
    def __init__(self):
        # Dictionary to track which memes have been shown for each category
        self.used_files = {}

    def get_random_meme(self, context_category):
        folder_path = os.path.join(LOCALDB_PATH, context_category)
        all_files = os.listdir(folder_path)
        image_files = [f for f in all_files if
                       f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))]

        if not image_files:
            raise ValueError("No image files found in the folder.")

        # Initialize usage tracking if not present
        if context_category not in self.used_files:
            self.used_files[context_category] = set()

        # Reset if we’ve shown all images in the current cycle
        if len(self.used_files[context_category]) == len(image_files):
            self.used_files[context_category] = set()

        # Choose from images that haven’t been shown in the current cycle
        available_files = [f for f in image_files if f not in self.used_files[context_category]]
        random_file = random.choice(available_files)
        self.used_files[context_category].add(random_file)

        random_path = os.path.join(folder_path, random_file)

        try:
            with open(random_path, 'rb') as file:
                file_data = file.read()
                return file_data  # Return bytes directly, not memoryview
        except IOError as e:
            raise IOError(f"Failed to read image file {random_file}: {str(e)}")

    def upload_file(self, context_category, picture_name, path_to_image):
        pass
