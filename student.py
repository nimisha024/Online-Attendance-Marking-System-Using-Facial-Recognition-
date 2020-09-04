from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from db.db_util import get_connection


class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('regNO',
                        required=True,
                        help='This field cannot be left blank'
                        )

    @jwt_required()
    def get(self, name):
        student = self.find_by_name(name)
        if student:
            return student
        return {'message': 'Student not found'}

    @staticmethod
    def find_by_name(name):
        connection = get_connection()
        cursor = connection.cursor()

        query = 'SELECT * FROM students WHERE name=?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'student': {'name': row[0], 'regNO': row[1], 'course': row[2]}}

    def post(self, name):
        if self.find_by_name(name):
            return {'message': f"A student with name '{name}' already exists."}, 400

        data = Student.parser.parse_args()

        student = {'name': name, 'regNO': data['regNO'], 'course': 'course'}

        try:
            self.insert(student)
        except:
            return {'message': 'An error occurred inserting the student id.'}, 500  # Internal server error

        return student, 201

    @staticmethod
    def insert(student):
        connection = get_connection()
        cursor = connection.cursor()

        query = 'INSERT INTO students VALUES (?, ?, ?)'
        cursor.execute(query, (student['name'], student['regNO'], student['course']))

        connection.commit()
        connection.close()

    @staticmethod
    def delete(name):
        connection = get_connection()
        cursor = connection.cursor()

        query = 'DELETE FROM students WHERE name=?'
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Student account deleted'}

    def put(self, name):
        data = Student.parser.parse_args()

        student = self.find_by_name(name)
        updated_student = {'name': name, 'regNO': data['regNO'], 'course': 'course'}

        if student is None:
            try:
                self.insert(updated_student)
            except:
                return {'message': 'An error occurred inserting the student id.'}, 500
        else:
            try:
                self.update(updated_student)
            except:
                return {'message': 'An error occurred updating the student id.'}, 500
        return updated_student

    @classmethod
    def update(cls, student):
        connection = get_connection()
        cursor = connection.cursor()

        query = 'UPDATE students SET regNO=? WHERE name=?'
        cursor.execute(query, (student['regNO'], student['name']))

        connection.commit()
        connection.close()


class StudentList(Resource):
    def get(self):
        connection = get_connection()
        cursor = connection.cursor()

        query = 'SELECT * FROM students'
        result = cursor.execute(query)
        students = []
        for row in result:
            students.append({'name': row[0], 'regNO': row[1], 'course': row[2]})

        connection.close()

        return {'students': students}
