from flask import jsonify, session
from flask_restful import Resource

import config
from student import Student
from degree import Minor

# Minor Completion API
# MC API for receiving minor completion for a student


class CheckMinorRequirements(Resource):
    def get(self, minor_name=""):
        if session.get("student") and session.get("minor"):
            student = Student.deserialize(session["student"])
            minor = Minor.deserialize(session["minor"])

            completion = minor.check_progress(student.get_courses)

            resp = jsonify({'completion': completion})
            resp.status_code = 200

        else:
            resp = jsonify(
                {'error': 'Either minor or student course list hasn\'t been set'})
            resp.status_code = 400

        return resp

    def post(self, minor_name=""):
        if session.get("student") and session.get("minor"):
            student = Student.deserialize(session["student"])
            minor = Minor.deserialize(session["minor"])

            completion = minor.check_progress(student.get_courses)

            resp = jsonify({'completion': completion})
            resp.status_code = 200

        else:
            resp = jsonify(
                {'error': 'Either minor or student course list hasn\'t been set'})
            resp.status_code = 400

        return resp
