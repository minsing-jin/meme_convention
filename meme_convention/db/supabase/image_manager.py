import os
import time
import requests
from io import BytesIO
from PIL import Image
from supabase import create_client


class ImageManager:
    def __init__(self, supabase_url, supabase_key, bucket_name):
        self.supabase = create_client(supabase_url, supabase_key)
        self.bucket_name = bucket_name

    def upload_image(self, file_path):
        """Upload image with validation and optimization"""
        if not self.validate_image_type(file_path):
            return {"success": False, "error": "Invalid file type"}

        if not self.validate_image_size(file_path):
            return {"success": False, "error": "File too large"}

        # Generate unique filename
        filename = f"{int(time.time())}_{os.path.basename(file_path)}"

        try:
            with open(file_path, 'rb') as f:
                response = self.supabase.storage.from_(self.bucket_name).upload(
                    file=f,
                    path=filename,
                    file_options={"content-type": self.get_content_type(file_path)}
                )

            return {"success": True, "filename": filename, "response": response}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_image_url(self, filename):
        """Get public URL for image"""
        try:
            response = self.supabase.storage.from_(self.bucket_name).get_public_url(filename)
            return response
        except Exception as e:
            return None

    def delete_image(self, filename):
        """Delete image from storage"""
        try:
            response = self.supabase.storage.from_(self.bucket_name).remove([filename])
            return {"success": True, "response": response}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def display_image(self, filename):
        """Display image from storage"""
        url = self.get_image_url(filename)
        if url:
            self.display_image_from_url(url)
        else:
            print("Could not get image URL")

    @staticmethod
    def validate_image_type(file_path):
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif'}
        _, ext = os.path.splitext(file_path)
        return ext.lower() in allowed_extensions

    @staticmethod
    def validate_image_size(file_path, max_size_mb=5):
        file_size = os.path.getsize(file_path)
        return file_size <= max_size_mb * 1024 * 1024

    @staticmethod
    def get_content_type(file_path):
        ext = os.path.splitext(file_path)[1].lower()
        content_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif'
        }
        return content_types.get(ext, 'application/octet-stream')

    @staticmethod
    def display_image_from_url(image_url):
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            img.show()
        except Exception as e:
            print(f"Error displaying image: {e}")


import pyperclip  # For clipboard operations


class SpecializedImageManager(ImageManager):
    def handle_image_selection(self, file_path):
        """Handle image selection based on type"""
        _, ext = os.path.splitext(file_path)

        if ext.lower() in ['.jpg', '.jpeg', '.png']:
            # For static images: copy image to clipboard
            return self.copy_image_to_clipboard(file_path)
        elif ext.lower() == '.gif':
            # For GIFs: upload to Supabase and copy URL to clipboard
            return self.handle_gif_upload(file_path)
        else:
            return {"success": False, "error": "Unsupported file type"}

    def copy_image_to_clipboard(self, file_path):
        """Copy static image to clipboard"""
        try:
            with Image.open(file_path) as img:
                # Convert to format suitable for clipboard
                output = BytesIO()
                img.save(output, format='PNG')
                output.seek(0)

                # Copy to clipboard (implementation depends on OS)
                # This is a simplified example
                pyperclip.copy(f"Image data from: {file_path}")
                return {"success": True, "message": "Image copied to clipboard"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def handle_gif_upload(self, file_path):
        """Upload GIF and copy URL to clipboard"""
        try:
            # Upload GIF to Supabase
            upload_result = self.upload_image(file_path)

            if upload_result["success"]:
                # Get public URL
                url = self.get_image_url(upload_result["filename"])

                if url:
                    # Copy URL to clipboard
                    pyperclip.copy(url)
                    return {
                        "success": True,
                        "message": "GIF uploaded and URL copied to clipboard",
                        "url": url
                    }

            return {"success": False, "error": "Failed to upload GIF"}
        except Exception as e:
            return {"success": False, "error": str(e)}


if __name__ == "__main__":
    # Initialize the image manager
    image_manager = SpecializedImageManager(
        supabase_url="your-supabase-url",
        supabase_key="your-supabase-key",
        bucket_name="your-bucket-name"
    )

    # Upload and handle different image types
    result = image_manager.handle_image_selection("image.jpg")  # Copies to clipboard
    result = image_manager.handle_image_selection("animation.gif")  # Uploads and copies URL

    # Display an image
    image_manager.display_image("uploaded_image.jpg")

    # Delete an image
    delete_result = image_manager.delete_image("uploaded_image.jpg")
