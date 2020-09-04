from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from security import authenticate, identity
from student import Student, StudentList
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'nimisha'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Student, '/student/<string:name>')
api.add_resource(StudentList, '/students')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
