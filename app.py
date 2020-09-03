from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'nimisha'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

students = []

class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('regNO',
                         required=True,
                         help="This field cannot be left blank"
                         )
    @jwt_required()
    def get(self, name):
        student = next(filter(lambda x: x['name'] == name, students), None)
        return {'student': student}, 200 if student else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, students), None):
            return {'message': "A student with name '{}' already exists.".format(name)}, 400

        data = Student.parser.parse_args()

        student = {'name': name, 'regNO': data['regNO'], 'course': 'CSE3001'}
        students.append(student)
        return student, 201

    def delete(self, name):
        global students
        students = list(filter(lambda x: x['name'] != name, students))
        return {'message': 'Student account deleted'}

    def put(self, name):
        data = Student.parser.parse_args()

        student = next(filter(lambda x: x['name'] == name, students), None)
        if student is None :
            item = {'name': name, 'regNO': data['regNO'], 'course': 'CSE2001'}
            students.append(student)
        else:
            student.update(data)
        return student

class StudentList(Resource):
    def get(self):
        return {'students':students}

api.add_resource(Student, '/student/<string:name>')
api.add_resource(StudentList, '/students')

app.run(port=5000, debug=True)
