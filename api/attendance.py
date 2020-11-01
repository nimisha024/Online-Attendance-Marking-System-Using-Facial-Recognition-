import os

import werkzeug
from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse

from db.db_util import get_student, mark_attendance_present, does_teach_course, \
    get_course_attendance, \
    has_enrolled_course, has_ongoing_class, end_class, start_class, get_class_id, get_present_students, \
    mark_attendance_absent, get_all_students, get_student_attendance
from facial_recog.config import TO_BE_PROCESSED_IMG_DIR
from facial_recog.facial_recognition import fr


class Attendance(Resource):
    @jwt_required()
    def get(self, course_id):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=False)
        args = parser.parse_args()

        if current_identity.is_student:
            user_id = args['user_id']
            if user_id:
                if user_id == current_identity.id:
                    return get_student_attendance(course_id, user_id), 200
                else:
                    return {'message': 'You are not authorized to view this student\'s attendance details'}, 200
            else:
                return {'message': 'user_id must be passed to view student\'s attendance details'}, 404
        else:
            # Aggregate view of each student's percentage wise attendance will be returned
            user_id = current_identity.id
            if does_teach_course(course_id, user_id):
                attendance = get_course_attendance(course_id)
                for row in attendance:
                    row.update(get_student(row['student_id']))
                    row["attendance_percent"] = round(row["present_count"] * 100 / row["total_count"], 4)
                return attendance, 200
            else:
                return {'message': 'You do not teach this course, hence cannot view it\'s attendance details'}, 200

    @jwt_required()
    def post(self, course_id):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True)
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', required=False)
        args = parser.parse_args()

        user_id = args['user_id']
        image_file = args['file']

        if user_id == current_identity.id:
            if current_identity.is_student:
                if has_enrolled_course(course_id, user_id):
                    if has_ongoing_class(course_id):
                        image_file.save(os.path.join(TO_BE_PROCESSED_IMG_DIR, user_id))
                        match = fr.recognize_face(user_id)
                        if match == user_id:
                            mark_attendance_present(course_id, user_id)
                            return {'message': 'Your attendance was marked successfully'}, 200
                        else:
                            return {'message': 'You were not found in the image'}, 200
                    else:
                        return {'message': 'Course has no active class'}, 200
                else:
                    return {'message': 'You are not enrolled in this course'}, 200
            else:
                if has_ongoing_class(course_id):
                    class_id = get_class_id(course_id)
                    all_students = get_all_students(course_id)
                    present_students = get_present_students(class_id)
                    absent_students = [student for student in all_students if student not in present_students]
                    mark_attendance_absent(class_id, absent_students)
                    end_class(course_id)
                    return {'message': 'Class ended successfully'}, 200
                else:
                    start_class(course_id)
                    return {'message': 'Class started successfully'}, 200
        else:
            return {'message': 'You can only add your own attendance'}, 200
