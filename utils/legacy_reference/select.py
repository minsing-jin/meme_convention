import psycopg2
from PIL import Image
import io

if __name__ == "__main__":
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            database="meme_collection",
            user="myuser",
            password="test",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Select picture where id = 1
        cursor.execute("SELECT picture_name FROM memes WHERE id = %s", (1,))
        result = cursor.fetchone()

        if result and result[0]:
            picture_data = result[0]

            # Save the picture to a local file
            with open('retrieved_picture.gif', 'wb') as file:
                file.write(picture_data)

            print("Picture saved successfully as 'retrieved_picture.gif'.")

            # Optionally display the picture using Pillow
            img = Image.open(io.BytesIO(picture_data))
            img.show()

        else:
            print("No picture found for the given ID.")

    except psycopg2.Error as e:
        print(f"Database error: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
