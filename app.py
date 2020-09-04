from flask import Flask
from flask_jwt import JWT
from flask_restful import Resource, Api

from security import authenticate, identity
from student import Student
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'nimisha'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

students = []


class StudentList(Resource):
    @staticmethod
    def get():
        return {'students': students}


api.add_resource(Student, '/student/<string:name>')
api.add_resource(StudentList, '/students')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
