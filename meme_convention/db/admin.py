import psycopg2

def create_table():
    """
    Create a table in PostgreSQL database to store memes.
    :return:
    """

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

        print("Connected to PostgreSQL successfully!")

        # Create table query
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS memes (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                picture BYTEA
            );
        '''

        # Execute the query
        cursor.execute(create_table_query)
        conn.commit()

        print("Table created successfully!")

    except psycopg2.Error as e:
        print(f"Database error: {e}")

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()