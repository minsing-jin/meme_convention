import psycopg2
from meme_convention.db.base import BASEDB
from PIL import Image
import io


class User(BASEDB):
    # TODO: I add recommendation system, implement user preferences and history tracking
    def __init__(self, username, password):
        super().__init__()
        self.cursor = self.conn.cursor()
        # TODO: It will be implemented in the future
        self.username = username
        self.password = password

    def get_random_meme(self, context_category):
        try:
            self.cursor.execute(
                "SELECT Id, context_category, picture_name, data_binary "
                "FROM memes WHERE context_category = %s "
                "ORDER BY RANDOM() LIMIT 1;",
                (context_category,)
            )
            meme = self.cursor.fetchone()

            return meme
        except psycopg2.Error as e:
            print(f"Error retrieving random meme: {e}")
            return None

    def upload_meme(self, context_category, picture_name, path_to_image):
        try:
            with open(path_to_image, 'rb') as file:
                image_data = file.read()
            self.cursor.execute(
                "INSERT INTO memes (context_category, picture_name, data_binary) "
                "VALUES (%s, %s, %s);",
                (context_category, picture_name, psycopg2.Binary(image_data))
            )
            self.conn.commit()

            print("Meme uploaded successfully!")
            file.close()
        except psycopg2.Error as e:
            print(f"Error uploading meme: {e}")
            self.conn.rollback()
