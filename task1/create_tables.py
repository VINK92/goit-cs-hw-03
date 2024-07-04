import psycopg2

def create_tables():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS status (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            status_id INTEGER NOT NULL REFERENCES status(id),
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
        )
        """
    ]

    conn = None
    try:
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(
            dbname="task_management",
            user="your_username",
            password="your_password",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        for command in commands:
            print(f"Executing command: {command}")
            cur.execute(command)
        cur.close()
        conn.commit()
        print("Tables created successfully!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")

if __name__ == '__main__':
    create_tables()
