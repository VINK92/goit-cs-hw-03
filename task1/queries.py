import psycopg2


def execute_queries():
    queries = [
        # Отримати всі завдання певного користувача
        ("SELECT * FROM tasks WHERE user_id = %s;", (1,)),

        # Вибрати завдання за певним статусом
        ("SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = %s);", ('new',)),

        # Оновити статус конкретного завдання
        ("UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = %s) WHERE id = %s;", ('in progress', 1)),

        # Отримати список користувачів, які не мають жодного завдання
        ("SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);", ()),

        # Додати нове завдання для конкретного користувача
        ("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);",
         ('New Task', 'Task Description', 1, 1)),

        # Отримати всі завдання, які ще не завершено
        ("SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = %s);", ('completed',)),

        # Видалити конкретне завдання
        ("DELETE FROM tasks WHERE id = %s;", (1,)),

        # Знайти користувачів з певною електронною поштою
        ("SELECT * FROM users WHERE email LIKE %s;", ('%@example.com',)),

        # Оновити ім'я користувача
        ("UPDATE users SET fullname = %s WHERE id = %s;", ('New Name', 1)),

        # Отримати кількість завдань для кожного статусу
        (
        "SELECT status.name, COUNT(*) FROM tasks INNER JOIN status ON tasks.status_id = status.id GROUP BY status.name;",
        ()),

        # Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
        ("SELECT tasks.* FROM tasks INNER JOIN users ON tasks.user_id = users.id WHERE users.email LIKE %s;",
         ('%@example.com',)),

        # Отримати список завдань, що не мають опису
        ("SELECT * FROM tasks WHERE description IS NULL;", ()),

        # Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
        (
        "SELECT users.fullname, tasks.title FROM tasks INNER JOIN users ON tasks.user_id = users.id WHERE tasks.status_id = (SELECT id FROM status WHERE name = %s);",
        ('in progress',)),

        # Отримати користувачів та кількість їхніх завдань
        (
        "SELECT users.fullname, COUNT(tasks.id) FROM users LEFT JOIN tasks ON users.id = tasks.user_id GROUP BY users.fullname;",
        ())
    ]

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
        for query, params in queries:
            cur.execute(query, params)
            if query.strip().upper().startswith("SELECT"):
                results = cur.fetchall()
                for row in results:
                    print(row)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    execute_queries()
