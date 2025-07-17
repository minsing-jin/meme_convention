import requests
from io import BytesIO


def get_image_from_supabase(bucket_name, file_path):
    """Get image from Supabase storage"""
    try:
        # Get public URL
        response = supabase.storage.from_(bucket_name).get_public_url(file_path)
        return response
    except Exception as e:
        print(f"Error getting image URL: {e}")
        return None


def display_image_from_url(image_url):
    """Display image from URL"""
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content))
        img.show()
    except Exception as e:
        print(f"Error displaying image from URL: {e}")
