import io
from typing import Any

from PIL import Image, ImageSequence
from meme_convention.db.postgresql.postgresql import POSTGRESQL


def sample_image_upload(context_category, picture_name, path_to_image):
    user = POSTGRESQL()
    # # Example usage
    user.upload_meme(context_category, picture_name, path_to_image)

    meme = user.get_random_meme("pr")
    if meme:
        img = Image.open(io.BytesIO(bytes(meme[-1])))
        img.show()
    else:
        print("No memes found for the specified category.")

def extract_gif_frames(img):
    return [frame.copy() for frame in ImageSequence.Iterator(img)]
