import os
from datetime import timedelta

from flask import Flask, render_template, send_from_directory
from flask_jwt import JWT, jwt_required
from flask_restful import Resource, Api

from api.student import Student
from api.student_courses import StudentCourses
from api.user import UserRegister, UserApi
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'nimisha'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3000)
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

students = []


# @app.route('/<string:page_name>/')
# def render_static(page_name):
#     return render_template(f'{page_name}.html')

@app.route('/login')
def login():
    return render_template('login.html')


@jwt_required()
@app.route('/course')
def course():
    return render_template('course.html')


@jwt_required()
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


class StudentList(Resource):
    @staticmethod
    def get():
        return {'students': students}


api.add_resource(UserApi, '/api/user/')
api.add_resource(Student, '/api/student/<int:user_id>')
api.add_resource(StudentCourses, '/api/student/<int:user_id>/courses')
api.add_resource(StudentList, '/api/students')
api.add_resource(UserRegister, '/api/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
