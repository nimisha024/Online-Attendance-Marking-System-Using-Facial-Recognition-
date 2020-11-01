import os
import sqlite3


def get_connection():
    db_file = os.path.join(os.getcwd(), 'db', 'data.db')
    return sqlite3.connect(db_file, isolation_level=None)


def get_student(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = 'SELECT id, student_id, student_name FROM student WHERE id=?'
    result = cursor.execute(query, (user_id,))
    row = result.fetchone()
    connection.close()

    if row:
        student = {'id': row[0], 'student_id': row[1], 'student_name': row[2]}
    else:
        student = None

    connection.close()
    return student


def get_faculty(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = 'SELECT id, faculty_id, faculty_name FROM faculty WHERE id=?'
    result = cursor.execute(query, (user_id,))
    row = result.fetchone()
    if row:
        faculty = {'id': row[0], 'faculty_id': row[1], 'faculty_name': row[2]}
    else:
        faculty = None

    connection.close()
    return faculty


def get_course(course_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = 'SELECT course_id, course_name, faculty_id FROM course WHERE course_id=?'
    result = cursor.execute(query, (course_id,))
    row = result.fetchone()
    if row:
        course = {'course_id': row[0], 'course_name': row[1], 'faculty_id': row[2]}
    else:
        course = None

    connection.close()
    return course


def get_student_courses(student_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = 'SELECT course_id FROM student_course WHERE student_id=?'
    result = cursor.execute(query, (student_id,))
    rows = result.fetchall()
    connection.close()

    student_courses = []
    for row in rows:
        student_courses.append(row[0])

    return student_courses

def get_faculty_courses(faculty_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = 'SELECT course_id FROM course WHERE faculty_id=?'
    result = cursor.execute(query, (faculty_id,))
    rows = result.fetchall()
    connection.close()

    faculty_courses = []
    for row in rows:
        faculty_courses.append(row[0])

    return faculty_courses
