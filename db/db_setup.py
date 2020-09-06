from db.db_util import get_connection


def setup():
    create_tables()
    insert_users()


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    create_table = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)'
    cursor.execute(create_table)

    create_table = 'CREATE TABLE IF NOT EXISTS students (name text, regNO text, course text)'
    cursor.execute(create_table)

    connection.close()


def insert_users():
    connection = get_connection()
    cursor = connection.cursor()

    insert_query = "INSERT INTO users VALUES (?, ?, ?)"
    users = [
        (1, 'nimisha', 'asdf'),
        (2, 'tanay', 'asdf'),
        (3, 'daksh', 'xyz')
    ]

    cursor.executemany(insert_query, users)

    select_query = "SELECT * FROM users"
    for row in cursor.execute(select_query):
        print(row)

    connection.close()


if __name__ == "__main__":
    setup()
