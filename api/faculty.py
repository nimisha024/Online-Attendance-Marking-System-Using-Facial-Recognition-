from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse

from db.db_util import get_connection, get_faculty


class Faculty(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', required=True, help='ID field cannot be left blank')

    @jwt_required()
    def get(self, user_id):
        if current_identity.id == user_id and not current_identity.is_student:
            faculty = get_faculty(user_id)
            if faculty:
                return faculty
            return {'message': 'Faculty not found'}, 404
        else:
            return {'message': 'Current user is not authorized to view this Faculty\'s details'}, 404

    def post(self, name):
        if self.find_by_name(name):
            return {'message': f"A Faculty with name '{name}' already exists."}, 400

        data = Faculty.parser.parse_args()

        faculty = {'name': name, 'regNO': data['regNO'], 'course': 'course'}

        try:
            self.insert(faculty)
        except:
            return {'message': 'An error occurred inserting the faculty id.'}, 500  # Internal server error

        return faculty, 201

    @staticmethod
    def insert(faculty):
        connection = get_connection()
        cursor = connection.cursor()

        query = 'INSERT INTO faculty VALUES (?, ?, ?)'
        cursor.execute(query, (faculty['name'], faculty['regNO'], faculty['course']))

        connection.commit()
        connection.close()

    @staticmethod
    def delete(name):
        connection = get_connection()
        cursor = connection.cursor()

        query = 'DELETE FROM faculty WHERE faculty_name=?'
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Faculty account deleted'}

    def put(self, name):
        data = Faculty.parser.parse_args()

        faculty = self.find_by_name(name)
        updated_faculty = {'name': name, 'regNO': data['regNO'], 'course': 'course'}

        if faculty is None:
            try:
                self.insert(updated_faculty)
            except:
                return {'message': 'An error occurred inserting the faculty id.'}, 500
        else:
            try:
                self.update(updated_faculty)
            except:
                return {'message': 'An error occurred updating the faculty id.'}, 500
        return updated_faculty

    @classmethod
    def update(cls, faculty):
        connection = get_connection()
        cursor = connection.cursor()

        query = 'UPDATE faculty SET regNO=? WHERE faculty_name=?'
        cursor.execute(query, (faculty['regNO'], faculty['name']))

        connection.commit()
        connection.close()


class FacultyList(Resource):
    def get(self):
        connection = get_connection()
        cursor = connection.cursor()

        query = 'SELECT * FROM faculty'
        result = cursor.execute(query)

        faculty = []
        for row in result:
            faculty.append({'name': row[0], 'regNO': row[1], 'course': row[2]})

        connection.close()

        return {'faculty': faculty}
