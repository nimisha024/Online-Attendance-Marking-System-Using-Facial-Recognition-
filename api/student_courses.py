from flask_jwt import jwt_required, current_identity
from flask_restful import Resource

from db.db_util import get_student, get_student_courses, get_course


class StudentCourses(Resource):
    @jwt_required()
    def get(self, user_id):
        if user_id == current_identity.id:
            student = get_student(user_id)
            student_courses = get_student_courses(student["student_id"])
            if student_courses:
                courses_list = []
                for course in student_courses:
                    courses_list.append(get_course(course))
                return courses_list
            return {'message': 'Student\'s courses not found'}, 404
        else:
            return {'message': 'Current student is not authorized to view this student\'s courses'}, 404
