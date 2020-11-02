from datetime import datetime, timedelta

from db.db_util import get_connection


def setup():
    create_tables()
    insert_users()
    insert_students()
    insert_faculties()
    insert_courses()
    insert_student_courses()
    insert_classes()
    insert_attendance()


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    create_table = 'CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, is_student BOOLEAN DEFAULT FALSE)'
    cursor.execute(create_table)

    create_table = 'CREATE TABLE IF NOT EXISTS student (id INTEGER PRIMARY KEY, student_id TEXT NOT NULL UNIQUE, student_name TEXT NOT NULL, FOREIGN KEY (id) REFERENCES user (id))'
    cursor.execute(create_table)

    create_table = 'CREATE TABLE IF NOT EXISTS faculty (id INTEGER PRIMARY KEY, faculty_id TEXT NOT NULL UNIQUE, faculty_name TEXT NOT NULL, FOREIGN KEY (id) REFERENCES user (id))'
    cursor.execute(create_table)

    create_table = 'CREATE TABLE IF NOT EXISTS course (id INTEGER PRIMARY KEY AUTOINCREMENT, course_code TEXT NOT NULL UNIQUE, course_name TEXT NOT NULL, faculty_id INTEGER NOT NULL, FOREIGN KEY (faculty_id) REFERENCES faculty (id))'
    cursor.execute(create_table)

    create_table = 'CREATE TABLE IF NOT EXISTS student_course (student_id INTEGER NOT NULL, course_id INTEGER NOT NULL, PRIMARY KEY (student_id, course_id), FOREIGN KEY (student_id) REFERENCES student (id), FOREIGN KEY (course_id) REFERENCES course (id))'
    cursor.execute(create_table)

    create_table = 'CREATE TABLE IF NOT EXISTS class (id INTEGER PRIMARY KEY AUTOINCREMENT, course_id INTEGER, start_time TIMESTAMP NOT NULL, end_time TIMESTAMP, FOREIGN KEY (course_id) REFERENCES course (id))'
    cursor.execute(create_table)

    create_table = 'CREATE TABLE IF NOT EXISTS attendance (class_id INTEGER, student_id INTEGER, is_present BOOLEAN DEFAULT TRUE, PRIMARY KEY (student_id, class_id), FOREIGN KEY (class_id) REFERENCES class (id), FOREIGN KEY (student_id) REFERENCES student (id))'
    cursor.execute(create_table)

    connection.close()


def insert_users():
    connection = get_connection()
    cursor = connection.cursor()

    insert_query = "INSERT INTO user (username, password, is_student) VALUES (?, ?, ?)"

    users = [
        ('nimisha', 'asdf', True),
        ('tanay', 'asdf', True),
        ('daksh', 'xyz', True),
        ('sumit', 'xyz', True),
        ('kavya', 'xyz', True),
        ('anisha', 'xyz', True),
        ('himanshu', 'xyz', True),
        ('ankita', 'xyz', True),
        ('stuti', 'xyz', True),
        ('parth', 'xyz', True),
        ('amit', 'xyz', False),
        ('kunal', 'xyz', False),
        ('pooja', 'xyz', False),
        ('manas', 'xyz', False),
        ('priya', 'xyz', False)
    ]
    cursor.executemany(insert_query, users)

    connection.close()


def insert_students():
    connection = get_connection()
    cursor = connection.cursor()

    insert_query = "INSERT INTO student (id, student_id, student_name) VALUES (?, ?, ?)"
    students = [
        (1, '19BCE1860', 'nimisha'),
        (2, '19BCE1563', 'tanay'),
        (3, '19BCE1320', 'daksh'),
        (4, '19BCE1600', 'sumit'),
        (5, '19BCE1426', 'kavya'),
        (6, '19BCE1123', 'anisha'),
        (7, '19BCE1024', 'himanshu'),
        (8, '19BCE1480', 'ankita'),
        (9, '19BCE1725', 'stuti'),
        (10, '19BCE1670', 'parth')

    ]

    cursor.executemany(insert_query, students)

    connection.close()


def insert_faculties():
    connection = get_connection()
    cursor = connection.cursor()

    insert_query = "INSERT INTO faculty (id, faculty_id, faculty_name) VALUES (?, ?, ?)"
    faculties = [
        (11, '11FAC1078', 'amit'),
        (12, '12FAC1346', 'kunal'),
        (13, '12FAC1005', 'pooja'),
        (14, '16FAC1089', 'manas'),
        (15, '18FAC1234', 'priya')

    ]

    cursor.executemany(insert_query, faculties)

    connection.close()


def insert_courses():
    connection = get_connection()
    cursor = connection.cursor()

    insert_query = "INSERT INTO course (course_code, course_name, faculty_id) VALUES (?, ?, ?)"
    courses = [
        ('CSE2003', 'Data Structure And Algorithm', 12),
        ('CSE3001', 'Software Engineering', 15),
        ('CSE3002', 'Internet And Web Programming', 11),
        ('PHY1002', 'Engineering Physics', 14),
        ('STS1102', 'Soft Skills', 13)
    ]

    cursor.executemany(insert_query, courses)

    connection.close()


def insert_student_courses():
    connection = get_connection()
    cursor = connection.cursor()

    insert_query = "INSERT INTO student_course (student_id, course_id) VALUES (?, ?)"
    student_courses = [
        (1, 1),
        (1, 2),
        (2, 3),
    ]

    cursor.executemany(insert_query, student_courses)

    connection.close()


def insert_classes():
    connection = get_connection()
    cursor = connection.cursor()

    insert_query = "INSERT INTO class (course_id, start_time, end_time) VALUES (?, ?, ?)"
    classes = [
        (1, datetime.now() - timedelta(days=1), datetime.now()),
    ]

    cursor.executemany(insert_query, classes)

    connection.close()


def insert_attendance():
    connection = get_connection()
    cursor = connection.cursor()

    insert_query = "INSERT INTO attendance (student_id, class_id) VALUES (?, ?)"
    attendance = [
        (1, 1),
        (1, 2),
    ]

    cursor.executemany(insert_query, attendance)

    connection.close()


if __name__ == "__main__":
    setup()
