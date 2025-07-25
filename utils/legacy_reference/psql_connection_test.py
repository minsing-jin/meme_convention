import psycopg2

if __name__ == "__main__":
    try:
        conn = psycopg2.connect(
            database="meme_collection",
            user="myuser",
            password="test",
            host="localhost",
            port="5432"
        )
        print("Connected to PostgreSQL successfully!")

    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
