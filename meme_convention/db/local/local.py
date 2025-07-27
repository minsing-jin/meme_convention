import os
import random
from pathlib import Path

LOCALDB_PATH = os.path.join(Path("./").parent, 'resources', 'local_db')

class LocalDB:
    def __init__(self):
        pass

    def get_random_meme(self, context_category):
        """
        Selects a random image from folder and returns it as bytes object.
        Compatible with database function that returns bytes.
        """
        all_files = os.listdir(os.path.join(LOCALDB_PATH, context_category))
        image_files = [f for f in all_files if
                       f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))]

        if not image_files:
            raise ValueError("No image files found in the folder.")

        random_file = random.choice(image_files)
        random_path = os.path.join(LOCALDB_PATH, context_category, random_file)

        try:
            with open(random_path, 'rb') as file:
                file_data = file.read()
                return file_data  # Return bytes directly, not memoryview
        except IOError as e:
            raise IOError(f"Failed to read image file {random_file}: {str(e)}")

    def upload_file(self, context_category, picture_name, path_to_image):
        pass
