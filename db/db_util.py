import os
import sqlite3
from datetime import datetime


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

    return student


def get_faculty(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = 'SELECT id, faculty_id, faculty_name FROM faculty WHERE id=?'
    result = cursor.execute(query, (user_id,))
    row = result.fetchone()
    connection.close()

    if row:
        faculty = {'id': row[0], 'faculty_id': row[1], 'faculty_name': row[2]}
    else:
        faculty = None

    return faculty


def get_course(course_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = 'SELECT course_code, course_name, faculty_id FROM course WHERE id=?'
    result = cursor.execute(query, (course_id,))
    row = result.fetchone()
    connection.close()

    if row:
        course = {'course_code': row[0], 'course_name': row[1], 'faculty_id': row[2]}
    else:
        course = None

    return course


def get_course_id(course_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = 'SELECT id FROM course WHERE course_code=?'
    result = cursor.execute(query, (course_id,))
    course = result.fetchone()
    connection.close()

    return course[0] if course else None


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

    query = 'SELECT id FROM course WHERE faculty_id=?'
    result = cursor.execute(query, (faculty_id,))
    rows = result.fetchall()
    connection.close()

    faculty_courses = []
    for row in rows:
        faculty_courses.append(row[0])

    return faculty_courses


def get_all_students(course_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = 'SELECT student_id FROM student_course WHERE course_id=?'
    result = cursor.execute(query, (course_id,))
    rows = result.fetchall()
    connection.close()

    course_students = []
    for row in rows:
        course_students.append(row[0])

    return course_students


def has_enrolled_course(course_id, student_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = 'SELECT course_id FROM student_course WHERE course_id=? and student_id=?'
    result = cursor.execute(query, (course_id, student_id,))
    rows = result.fetchall()
    connection.close()

    return len(rows) > 0


def does_teach_course(course_id, faculty_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = 'SELECT id FROM course WHERE id=? and faculty_id=?'
    result = cursor.execute(query, (course_id, faculty_id,))
    rows = result.fetchall()
    connection.close()

    return len(rows) > 0


def start_class(course_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = 'INSERT INTO class(course_id, start_time) values (?, ?)'
    cursor.execute(query, (course_id, datetime.now()))
    connection.close()


def end_class(course_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = 'UPDATE class set end_time = ? WHERE course_id = ? AND start_time IS NULL'
    cursor.execute(query, (datetime.now(), course_id))
    connection.close()


def has_ongoing_class(course_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = 'SELECT course_id FROM class WHERE course_id=? and end_time IS NULL'
    result = cursor.execute(query, (course_id,))
    rows = result.fetchall()
    connection.close()

    return len(rows) > 0


def get_class_id(course_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = 'SELECT course_id FROM class WHERE course_id=? and end_time IS NULL'
    result = cursor.execute(query, (course_id,))
    class_id = result.fetchone()[0]
    connection.close()

    return class_id


def get_attendance(course_id):
    # TODO student - present - total
    student_ids = get_all_students(course_id)

    student_attendance = {}
    for student_id in student_ids:
        student_attendance[student_id] = get_attendance(course_id, student_id)

    return student_attendance


def get_attendance(course_id, student_id):
    # TODO date - present
    connection = get_connection()
    cursor = connection.cursor()

    query = 'SELECT  strftime("%Y-%m-%dT%H:00:00.000", datetime) as hour FROM attendance WHERE student_id=? GROUP BY hour'
    result = cursor.execute(query, (course_id, student_id))
    rows = result.fetchall()
    connection.close()

    attendance = []
    for row in rows:
        attendance.append(row)

    return attendance


def get_present_students(class_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = 'SELECT student_id FROM attendance WHERE class_id=? AND is_present = TRUE'
    result = cursor.execute(query, (class_id,))
    rows = result.fetchall()
    connection.close()

    present_students = []
    for row in rows:
        present_students.append(row[0])

    return present_students


def mark_attendance_present(course_id, student_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = 'INSERT OR IGNORE INTO attendance(class_id, student_id, is_present) values (?, ?, ?)'
    cursor.execute(query, (course_id, student_id, True))
    connection.close()


def mark_attendance_absent(class_id, student_ids):
    connection = get_connection()
    cursor = connection.cursor()

    query = 'INSERT INTO attendance(class_id, student_id, is_present) values (?, ?, ?)'
    records = [(class_id, student_id, False) for student_id in student_ids]
    cursor.executemany(query, records)
    connection.close()
