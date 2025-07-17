def delete_local_image(file_path):
    """Delete image file from local filesystem"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")
            return True
        else:
            print(f"File not found: {file_path}")
            return False
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False

def delete_images_by_extension(folder_path, extension='.png'):
    """Delete all images of specific extension from folder"""
    try:
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(extension.lower()):
                file_path = os.path.join(folder_path, filename)
                os.remove(file_path)
                print(f"Deleted: {filename}")
    except Exception as e:
        print(f"Error deleting images: {e}")

def delete_image_from_supabase(bucket_name, file_path):
    """Delete image from Supabase storage"""
    try:
        response = supabase.storage.from_(bucket_name).remove([file_path])
        print(f"Deleted from Supabase: {file_path}")
        return response
    except Exception as e:
        print(f"Error deleting from Supabase: {e}")
        return None
