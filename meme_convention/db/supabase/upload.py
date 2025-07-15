from PIL import Image
import os
import io
from supabase import create_client, Client

# Supabase configuration
SUPABASE_URL = "your-supabase-url"
SUPABASE_KEY = "your-supabase-key"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def validate_image_type(file_path):
    """Validate if file is a supported image type"""
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif'}
    _, ext = os.path.splitext(file_path)
    return ext.lower() in allowed_extensions

def validate_image_size(file_path, max_size_mb=5):
    """Validate file size (default 5MB limit)"""
    file_size = os.path.getsize(file_path)
    return file_size <= max_size_mb * 1024 * 1024

def upload_image_to_supabase(file_path, bucket_name, file_name):
    """Upload image to Supabase storage"""
    try:
        with open(file_path, 'rb') as f:
            response = supabase.storage.from_(bucket_name).upload(
                file=f,
                path=file_name,
                file_options={"content-type": "image/jpeg"}
            )
        return response
    except Exception as e:
        print(f"Upload failed: {e}")
        return None


def process_and_upload_image(file_path, bucket_name):
    """Process image and upload to Supabase"""
    if not validate_image_type(file_path):
        return {"error": "Invalid file type"}

    if not validate_image_size(file_path):
        return {"error": "File too large"}

    # Optimize image before upload
    with Image.open(file_path) as img:
        # Resize if too large
        if img.width > 1920 or img.height > 1920:
            img.thumbnail((1920, 1920), Image.Resampling.LANCZOS)

        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Save optimized image
        output_path = f"optimized_{os.path.basename(file_path)}"
        img.save(output_path, "JPEG", optimize=True, quality=85)

    # Upload to Supabase
    result = upload_image_to_supabase(output_path, bucket_name, os.path.basename(output_path))

    # Clean up temporary file
    os.remove(output_path)

    return result
