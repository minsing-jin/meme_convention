import psycopg2
from abc import ABC, abstractmethod

class BASEDB(ABC):
    """
    Base class for database models.
    This class can be extended by other models to inherit common functionality.
    """
    def __init__(self, **kwargs):
        """
        Initialize the base model with keyword arguments.
        This method can be overridden by subclasses to handle specific initialization.
        """
        try:
            self.conn = psycopg2.connect(
                database="meme_collection",
                user="myuser",
                password="test",
                host="localhost",
                port="5432"
            )
            print("Connected to PostgreSQL successfully!")

        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL: {e}")

    def __del__(self):
        """
        Close the database connection.
        This method should be called when the database operations are complete.
        """
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
        else:
            print("No database connection to close.")
