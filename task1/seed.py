import psycopg2
from faker import Faker


def seed_data():
    fake = Faker()
    statuses = ['new', 'in progress', 'completed']

    conn = None
    try:
        conn = psycopg2.connect(
            dbname="task_management",
            user="your_username",
            password="your_password",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        # Вставка статусів
        for status in statuses:
            cur.execute("INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", (status,))

        # Вставка випадкових користувачів та завдань
        for _ in range(10):
            fullname = fake.name()
            email = fake.unique.email()
            cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s) RETURNING id;", (fullname, email))
            user_id = cur.fetchone()[0]

            for _ in range(3):
                title = fake.sentence(nb_words=5)
                description = fake.text(max_nb_chars=200)
                status_id = fake.random_element(elements=(1, 2, 3))
                cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);",
                            (title, description, status_id, user_id))

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    seed_data()
